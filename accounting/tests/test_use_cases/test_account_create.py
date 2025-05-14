from decimal import Decimal

import pytest

from accounting.models import Account
from accounting.use_cases import AccountCreateUseCase
from telegram_auth.exceptions import UserNotFoundError, InvalidInitialBalanceError
from telegram_auth.tests.factories import UserFactory

@pytest.mark.django_db
def test_account_successfully_created():
    user = UserFactory()

    result = AccountCreateUseCase(
        name="Samat",
        user_id=user.id,
        is_public=True,
        initial_balance=Decimal("1000.00")
    ).execute()

    assert result.name == "Samat"
    assert result.user_id == user.id
    assert result.is_public is True
    assert result.initial_balance == Decimal("1000.00")

    account = Account.objects.get(id=result.id)
    assert account.name == "Samat"
    assert account.user == user
    assert account.initial_balance == Decimal("1000.00")
    assert account.is_public is True


@pytest.mark.django_db
def test_account_create_user_not_found():
    non_existing_user_id = 9999

    with pytest.raises(UserNotFoundError):
        AccountCreateUseCase(
            name="Test",
            user_id=non_existing_user_id,
            is_public=False,
            initial_balance=Decimal("0.00")
        ).execute()