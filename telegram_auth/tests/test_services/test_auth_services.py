import datetime
import json
import time
import urllib.parse

import pytest

from telegram_auth.exceptions import (
    TelegramMiniAppInitDataExpiredError,
    TelegramMiniAppInitDataInvalidError,
    TelegramMiniAppInitDataRequiredError,
)
from telegram_auth.services import (
    ensure_init_data_not_expired,
    ensure_init_data_valid,
    parse_request_data,
    parse_init_data,
)


# Проверяет, что init_data не истекло (валидная дата)
def test_ensure_init_data_not_expired_valid(auth_date):
    ttl_in_seconds = 86400  # 24 часа

    ensure_init_data_not_expired(
        auth_date=auth_date,
        ttl_in_seconds=ttl_in_seconds,
    )

# Проверяет, что истекшее init_data вызывает исключение
def test_ensure_init_data_not_expired_invalid():
    old_auth_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=25)
    ttl_in_seconds = 86400  # 24 часа

    with pytest.raises(TelegramMiniAppInitDataExpiredError):
        ensure_init_data_not_expired(
            auth_date=old_auth_date,
            ttl_in_seconds=ttl_in_seconds,
        )

# Проверяет, что корректные init_data и токен проходят без ошибки
def test_ensure_init_data_valid_success(valid_init_data_string, bot_token):
    ensure_init_data_valid(
        init_data=valid_init_data_string,
        bot_token=bot_token,
    )

# Проверяет, что отсутствие hash вызывает ошибку
def test_ensure_init_data_valid_no_hash(bot_token):
    init_data = "auth_date=123456789&user=%7B%22id%22%3A123456789%7D"

    with pytest.raises(TelegramMiniAppInitDataInvalidError):
        ensure_init_data_valid(
            init_data=init_data,
            bot_token=bot_token,
        )

# Проверяет, что неверный hash вызывает ошибку
def test_ensure_init_data_valid_wrong_hash(bot_token):
    init_data = "auth_date=123456789&hash=invalid_hash&user=%7B%22id%22%3A123456789%7D"

    with pytest.raises(TelegramMiniAppInitDataInvalidError):
        ensure_init_data_valid(
            init_data=init_data,
            bot_token=bot_token,
        )

# Проверяет успешное извлечение init_data из словаря запроса
def test_parse_request_data_success():
    request_data = {"init_data": "valid_init_data"}

    result = parse_request_data(request_data)

    assert result == "valid_init_data"

# Проверяет, что при отсутствии ключа init_data выбрасывается исключение
def test_parse_request_data_missing_key():
    request_data = {"some_other_key": "value"}

    with pytest.raises(TelegramMiniAppInitDataRequiredError):
        parse_request_data(request_data)

# Проверяет, что при передаче списка вместо словаря выбрасывается исключение
def test_parse_request_data_list():
    request_data = []

    with pytest.raises(TelegramMiniAppInitDataRequiredError):
        parse_request_data(request_data)

# Проверяет успешный парсинг init_data со всеми параметрами
def test_parse_init_data(valid_init_data_string, telegram_user_data):
    result = parse_init_data(valid_init_data_string)

    assert result.user.id == telegram_user_data["id"]
    assert result.user.first_name == telegram_user_data["first_name"]
    assert result.user.last_name == telegram_user_data["last_name"]
    assert result.user.username == telegram_user_data["username"]
    assert isinstance(result.auth_date, datetime.datetime)

# Проверяет, что отсутствие username не вызывает исключения и username = None
def test_parse_init_data_missing_username(bot_token):
    user_data = {
        "id": 123456789,
        "first_name": "John",
        "last_name": "Doe",
        # username отсутствует
    }
    auth_date = int(time.time())
    params = {
        "auth_date": str(auth_date),
        "user": json.dumps(user_data),
        "hash": "dummy_hash"  # В этом тесте hash не проверяется
    }
    init_data = urllib.parse.urlencode(params)

    result = parse_init_data(init_data)

    assert result.user.id == user_data["id"]
    assert result.user.first_name == user_data["first_name"]
    assert result.user.last_name == user_data["last_name"]
    assert result.user.username is None