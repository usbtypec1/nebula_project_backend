import pytest

from telegram_auth.exceptions import UserNotFoundError
from telegram_auth.models import User
from telegram_auth.services import (
    InitDataUser,
    ensure_user_exists,
    upsert_user,
)
from telegram_auth.tests.factories import UserFactory


# Проверяет, что ensure_user_exists не вызывает исключение, если пользователь существует
@pytest.mark.django_db
def test_ensure_user_exists_success():
    user = UserFactory()
    ensure_user_exists(user.id)

# Проверяет, что ensure_user_exists вызывает UserNotFoundError, если пользователь не найден
@pytest.mark.django_db
def test_ensure_user_exists_error():
    with pytest.raises(UserNotFoundError):
        ensure_user_exists(999)

# Проверяет, что upsert_user создает нового пользователя, если его нет в базе
@pytest.mark.django_db
def test_upsert_user_creates_new_user(init_data):
    assert User.objects.filter(telegram_id=init_data.user.id).count() == 0

    user = upsert_user(init_data)

    assert user.telegram_id == init_data.user.id
    assert user.full_name == init_data.user.full_name
    assert user.username == init_data.user.username
    assert User.objects.filter(telegram_id=init_data.user.id).count() == 1

# Проверяет, что upsert_user обновляет существующего пользователя
@pytest.mark.django_db
def test_upsert_user_updates_existing_user(init_data):
    existing_user = UserFactory(
        telegram_id=init_data.user.id,
        full_name="Old Name",
        username="oldusername",
    )

    user = upsert_user(init_data)

    assert user.id == existing_user.id
    assert user.telegram_id == init_data.user.id
    assert User.objects.filter(telegram_id=init_data.user.id).count() == 1

# Проверяет корректное формирование full_name при наличии last_name
def test_init_data_user_full_name_with_last_name():
    user = InitDataUser(
        id=123456789,
        first_name="John",
        last_name="Doe",
        username="johndoe",
    )

    assert user.full_name == "John Doe"

# Проверяет корректное формирование full_name при отсутствии last_name
def test_init_data_user_full_name_without_last_name():
    user = InitDataUser(
        id=123456789,
        first_name="John",
        last_name=None,
        username="johndoe",
    )

    assert user.full_name == "John"