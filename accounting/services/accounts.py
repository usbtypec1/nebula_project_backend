import datetime
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from django.core.exceptions import ValidationError
from django.db.models import Sum

from accounting.exceptions import (
    AccountAccessDeniedError,
    AccountAlreadyExistsError, AccountNotFoundError,
)
from accounting.models import Account, Transfer


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


@dataclass(frozen=True, slots=True, kw_only=True)
class AccountRetrieveDto:
    id: int
    user_id: int
    name: str
    is_public: bool
    initial_balance: Decimal
    created_at: datetime.datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class AccountWithBalanceDto(AccountRetrieveDto):
    balance: Decimal


def get_account_by_id(account_id: int) -> AccountRetrieveDto:
    try:
        account = Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        raise AccountNotFoundError

    return AccountRetrieveDto(
        id=account.id,
        user_id=account.user_id,
        name=account.name,
        is_public=account.is_public,
        initial_balance=account.initial_balance,
        created_at=account.created_at,
    )


class HasUserId(Protocol):
    user_id: int


def ensure_user_has_access_to_account(
        *,
        user_id: int,
        account: HasUserId,
) -> None:
    if account.user_id != user_id:
        raise AccountAccessDeniedError


class HasId(Protocol):
    id: int


class HasInitialBalance(Protocol):
    initial_balance: Decimal


def compute_account_balance(account: HasId | HasInitialBalance) -> Decimal:
    sent_amount: Decimal = (
        Transfer.objects
        .filter(from_account_id=account.id)
        .aggregate(Sum('amount'))
    )['amount']

    received_amount: Decimal = (
        Transfer.objects
        .filter(to_account_id=account.id)
        .aggregate(total=Sum('amount'))
    )['amount']

    return account.initial_balance - sent_amount + received_amount


def get_account_with_balance_by_id(account_id: int) -> AccountWithBalanceDto:
    account = get_account_by_id(account_id)
    balance = compute_account_balance(account)
    return AccountWithBalanceDto(
        id=account.id,
        user_id=account.user_id,
        name=account.name,
        is_public=account.is_public,
        initial_balance=account.initial_balance,
        created_at=account.created_at,
        balance=balance,
    )


def delete_account_by_id(account_id: int) -> None:
    deleted_count, _ = Account.objects.filter(id=account_id).delete()
    if deleted_count == 0:
        raise AccountNotFoundError


def update_account_by_id(
        *,
        account_id: int,
        name: str,
        is_public: bool,
        initial_balance: Decimal,
) -> None:
    updated_count = Account.objects.filter(id=account_id).update(
        name=name,
        is_public=is_public,
        initial_balance=initial_balance,
    )
    if updated_count == 0:
        raise AccountNotFoundError
