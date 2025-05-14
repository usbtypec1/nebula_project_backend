import datetime
import hashlib
import hmac
import json
import urllib.parse

import pytest
from django.utils import timezone

from telegram_auth.services import (
    TelegramMiniAppInitData,
    InitDataUser,
)


# auth services
@pytest.fixture
def bot_token():
    return "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ"


@pytest.fixture
def current_time():
    return datetime.datetime.now(datetime.UTC)


@pytest.fixture
def auth_date():
    return datetime.datetime.now(datetime.UTC)


@pytest.fixture
def telegram_user_data():
    return {
        "id": 123456789,
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe"
    }


@pytest.fixture
def valid_init_data_string(telegram_user_data, bot_token):
    auth_date = int(timezone.now().timestamp())
    params = {
        "auth_date": str(auth_date),
        "user": json.dumps(telegram_user_data),
    }

    # Sort parameters and create data_check_string
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(params.items())
    )

    # Create secret key
    secret_key = hmac.new(
        key=b"WebAppData",
        msg=bot_token.encode(),
        digestmod=hashlib.sha256
    ).digest()

    # Calculate hash
    hash_value = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    # Add hash to params
    params["hash"] = hash_value

    return urllib.parse.urlencode(params)


# user services
@pytest.fixture
def init_data_user():
    return InitDataUser(
        id=123456789,
        first_name="John",
        last_name="Doe",
        username="johndoe",
    )


@pytest.fixture
def init_data(init_data_user):
    import datetime
    return TelegramMiniAppInitData(
        user=init_data_user,
        auth_date=datetime.datetime.now(datetime.UTC),
    )


# use cases
@pytest.fixture
def init_data_user():
    return InitDataUser(
        id=123456789,
        first_name="John",
        last_name="Doe",
        username="johndoe",
    )


@pytest.fixture
def init_data(init_data_user):
    import datetime
    return TelegramMiniAppInitData(
        user=init_data_user,
        auth_date=datetime.datetime.now(datetime.UTC),
    )

