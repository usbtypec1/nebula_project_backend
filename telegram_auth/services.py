import datetime
import hashlib
import hmac
import json
import urllib.parse
from dataclasses import dataclass
from typing import TypedDict

from rest_framework_simplejwt.tokens import RefreshToken

from telegram_auth.exceptions import (
    TelegramMiniAppInitDataExpiredError,
    TelegramMiniAppInitDataInvalidError,
    TelegramMiniAppInitDataRequiredError, UserNotFoundError,
)
from telegram_auth.models import User


class InitDataParams(TypedDict):
    auth_date: str


def ensure_init_data_not_expired(
        *,
        auth_date: datetime.datetime,
        ttl_in_seconds: int,
) -> None:
    now = datetime.datetime.now(datetime.UTC)
    is_expired = (now - auth_date).total_seconds() > ttl_in_seconds
    if is_expired:
        raise TelegramMiniAppInitDataExpiredError


def ensure_init_data_valid(
        *,
        init_data: str,
        bot_token: str,
) -> None:
    params = dict(urllib.parse.parse_qsl(init_data))
    received_hash = params.pop("hash", None)

    if not received_hash:
        raise TelegramMiniAppInitDataInvalidError

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(params.items())
    )

    secret_key = hmac.new(
        key=b"WebAppData",
        msg=bot_token.encode(),
        digestmod=hashlib.sha256
    ).digest()

    computed_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(computed_hash, received_hash):
        raise TelegramMiniAppInitDataInvalidError


def parse_request_data(request_data: dict | list) -> str:
    if isinstance(request_data, list):
        raise TelegramMiniAppInitDataRequiredError
    try:
        return request_data["init_data"]
    except KeyError:
        raise TelegramMiniAppInitDataRequiredError


@dataclass(frozen=True, slots=True, kw_only=True)
class InitDataUser:
    id: int
    first_name: str
    last_name: str | None
    username: str | None

    @property
    def full_name(self) -> str:
        if self.last_name is None:
            return self.first_name
        return f"{self.first_name} {self.last_name}"


@dataclass(frozen=True, slots=True, kw_only=True)
class TelegramMiniAppInitData:
    user: InitDataUser
    auth_date: datetime.datetime


def parse_init_data(init_data: str) -> TelegramMiniAppInitData:
    params = dict(urllib.parse.parse_qsl(init_data))
    user = json.loads(params["user"])

    telegram_id: int = user["id"]
    first_name: str = user["first_name"]
    last_name: str | None = user["last_name"] or None
    username: str | None = user["username"] or None

    auth_date = datetime.datetime.fromtimestamp(
        int(params["auth_date"]),
        tz=datetime.UTC,
    )

    return TelegramMiniAppInitData(
        user=InitDataUser(
            id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
        ),
        auth_date=auth_date,
    )


class TelegramAuthenticateResult(TypedDict):
    access_token: str
    refresh_token: str


@dataclass(frozen=True, slots=True, kw_only=True)
class TelegramAuthenticateInteractor:
    request_data: dict | list
    ttl_in_seconds: int
    bot_token: str

    def execute(self) -> TelegramAuthenticateResult:
        init_data = parse_request_data(self.request_data)

        ensure_init_data_valid(
            init_data=init_data,
            bot_token=self.bot_token,
        )

        init_data = parse_init_data(init_data)

        ensure_init_data_not_expired(
            auth_date=init_data.auth_date,
            ttl_in_seconds=self.ttl_in_seconds,
        )

        user, _ = User.objects.get_or_create(
            telegram_id=init_data.user.id,
            defaults={
                "full_name": init_data.user.full_name,
                "username": init_data.user.username,
            }
        )

        refresh = RefreshToken.for_user(user)

        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }


def ensure_user_exists(
        user_id: int,
) -> None:
    if not User.objects.filter(id=user_id).exists():
        raise UserNotFoundError
