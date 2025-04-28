import datetime
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from django.core.exceptions import ValidationError
from django.db import IntegrityError, models
from django.db.models import Case, Sum, When

from accounting.exceptions import (
    AccountAccessDeniedError,
    AccountAlreadyExistsError, AccountNotFoundError,
)
from accounting.models import Account, Category, Transaction, Transfer


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


@dataclass(frozen=True, slots=True, kw_only=True)
class AccountBalance:
    account_id: int
    balance: Decimal


def compute_account_balance(
        account: HasId | HasInitialBalance,
) -> AccountBalance:
    sent_amount: Decimal = (
        Transfer.objects
        .filter(from_account_id=account.id)
        .aggregate(Sum('amount'))
    ).get('amount', Decimal('0'))

    received_amount: Decimal = (
        Transfer.objects
        .filter(to_account_id=account.id)
        .aggregate(total=Sum('amount'))
    ).get('amount', Decimal('0'))

    balance_based_on_transactions = (
            Transaction.objects.filter(account_id=account.id)
            .aggregate(
                balance=Sum(
                    Case(
                        models.When(
                            category__type=Category.Type.INCOME,
                            then=models.F('amount')
                        ),
                        models.When(
                            category__type=Category.Type.EXPENSE,
                            then=models.F('amount') * -1
                        ),
                        output_field=models.DecimalField(
                            max_digits=10, decimal_places=2
                        ),
                    )
                )
            )['balance'] or 0
    )
    balance = (
            balance_based_on_transactions
            + account.initial_balance
            - sent_amount
            + received_amount
    )
    return AccountBalance(account_id=account.id, balance=balance)


def get_account_with_balance_by_id(account_id: int) -> AccountWithBalanceDto:
    account = get_account_by_id(account_id)
    account_balance = compute_account_balance(account)
    return AccountWithBalanceDto(
        id=account.id,
        user_id=account.user_id,
        name=account.name,
        is_public=account.is_public,
        initial_balance=account.initial_balance,
        created_at=account.created_at,
        balance=account_balance.balance,
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
    try:
        updated_count = Account.objects.filter(id=account_id).update(
            name=name,
            is_public=is_public,
            initial_balance=initial_balance,
        )
    except IntegrityError as error:
        if (
                error.args[0] == (
                'UNIQUE constraint failed: accounting_account.name, '
                'accounting_account.user_id')
        ):
            raise AccountAlreadyExistsError
        raise
    if updated_count == 0:
        raise AccountNotFoundError


def compute_account_balances(
        accounts: list[HasId | HasInitialBalance],
) -> list[AccountBalance]:
    account_ids = {account.id for account in accounts}

    sent_amounts = (
        Transfer.objects
        .filter(from_account_id__in=account_ids)
        .values('from_account_id')
        .annotate(amount=Sum('amount'))
    )

    received_amounts = (
        Transfer.objects
        .filter(to_account_id__in=account_ids)
        .values('to_account_id')
        .annotate(amount=Sum('amount'))
    )

    account_id_to_sent_amount = {
        entry['from_account_id']: entry['amount']
        for entry in sent_amounts
    }
    account_id_to_received_amount = {
        entry['to_account_id']: entry['amount']
        for entry in received_amounts
    }

    transaction_amounts = (
        Transaction.objects
        .filter(account_id__in=account_ids)
        .values('account_id')
        .annotate(
            amount=models.Sum(
                models.Case(
                    models.When(
                        category__type=Category.Type.INCOME,
                        then=models.F('amount')
                    ),
                    models.When(
                        category__type=Category.Type.EXPENSE,
                        then=models.F('amount') * -1
                    ), output_field=models.DecimalField(
                        max_digits=10, decimal_places=2
                    ),
                )
            )
        )
    )

    account_id_to_transaction_amount = {
        entry['account_id']: entry['amount']
        for entry in transaction_amounts
    }

    account_balances: list[AccountBalance] = []
    for account in accounts:
        sent_amount = account_id_to_sent_amount.get(account.id, Decimal('0'))
        received_amount = account_id_to_received_amount.get(
            account.id, Decimal('0')
        )
        transaction_amount = account_id_to_transaction_amount.get(
            account.id, Decimal('0')
        )

        balance = (account.initial_balance - sent_amount + received_amount +
                   transaction_amount)

        account_balances.append(
            AccountBalance(account_id=account.id, balance=balance)
        )

    return account_balances


@dataclass(frozen=True, slots=True, kw_only=True)
class AccountsWithBalanceDto:
    accounts: list[AccountWithBalanceDto]
    total_balance: Decimal


def get_accounts_with_balance_by_user_id(
        user_id: int,
) -> AccountsWithBalanceDto:
    accounts = Account.objects.filter(user_id=user_id).all()
    account_balances = compute_account_balances(accounts)
    account_id_to_balance = {
        account_balance.account_id: account_balance.balance
        for account_balance in account_balances
    }

    accounts = [
        AccountWithBalanceDto(
            id=account.id,
            user_id=account.user_id,
            name=account.name,
            is_public=account.is_public,
            initial_balance=account.initial_balance,
            created_at=account.created_at,
            balance=account_id_to_balance.get(account.id, Decimal('0')),
        )
        for account in accounts
    ]

    total_balance = sum(
        account_balance.balance for account_balance in account_balances
    )
    return AccountsWithBalanceDto(
        accounts=accounts,
        total_balance=total_balance,
    )
