from dataclasses import dataclass

from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from telegram_auth.services import (
    ensure_init_data_not_expired, ensure_init_data_valid, parse_init_data,
    parse_request_data, upsert_user,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class TelegramAuthenticateResult:
    access_token: str
    refresh_token: str
    access_token_expires: int
    refresh_token_expires: int


@dataclass(frozen=True, slots=True, kw_only=True)
class TelegramAuthenticateUseCase:
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

        if settings.ENSURE_TELEGRAM_INIT_DATA_NOT_EXPIRED:
            ensure_init_data_not_expired(
                auth_date=init_data.auth_date,
                ttl_in_seconds=self.ttl_in_seconds,
            )

        user = upsert_user(init_data)
        refresh = RefreshToken.for_user(user)

        return TelegramAuthenticateResult(
            access_token=str(refresh.access_token),
            refresh_token=str(refresh),
            access_token_expires=refresh.access_token.get('exp'),
            refresh_token_expires=refresh.get('exp'),
        )
