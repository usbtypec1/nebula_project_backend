import datetime
from dataclasses import dataclass
from decimal import Decimal

from django.core.exceptions import ValidationError

from accounting.exceptions import AccountAlreadyExistsError
from accounting.models import Account


@dataclass(frozen=True, slots=True, kw_only=True)
class AccountCreateResultDto:
    id: int
    name: str
    user_id: int
    is_public: bool
    initial_balance: Decimal
    created_at: datetime.datetime


def create_account(
        *,
        name: str,
        user_id: int,
        is_public: bool,
        initial_balance: Decimal,
) -> AccountCreateResultDto:
    account = Account(
        name=name,
        user_id=user_id,
        is_public=is_public,
        initial_balance=initial_balance,
    )
    try:
        account.full_clean()
    except ValidationError as error:
        if ('Account with this Account name and User already exists.' in
                error.messages):
            raise AccountAlreadyExistsError
        raise
    account.save()

    return AccountCreateResultDto(
        id=account.id,
        name=account.name,
        user_id=account.user_id,
        is_public=account.is_public,
        initial_balance=account.initial_balance,
        created_at=account.created_at,
    )
