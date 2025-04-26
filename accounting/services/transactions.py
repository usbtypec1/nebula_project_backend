import datetime
from dataclasses import dataclass
from decimal import Decimal

from django.db.models import Q

from accounting.exceptions import TransactionAccessDeniedError
from accounting.exceptions.transactions import TransactionNotFoundError
from accounting.models import Transaction


@dataclass(frozen=True, slots=True, kw_only=True)
class Pagination:
    taken_count: int
    skipped_count: int
    total_count: int


@dataclass(frozen=True, slots=True, kw_only=True)
class TransactionListItem:
    id: int
    account_id: int
    account_name: str
    category_id: int
    category_type: int
    category_name: str
    amount: Decimal
    description: str | None
    date: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class TransactionsPage:
    transactions: list[TransactionListItem]
    pagination: Pagination


def map_transaction_to_list_item(
        transaction: Transaction,
) -> TransactionListItem:
    return TransactionListItem(
        id=transaction.id,
        account_id=transaction.account.id,
        account_name=transaction.account.name,
        category_id=transaction.category.id,
        category_type=transaction.category.type,
        category_name=transaction.category.name,
        amount=transaction.amount,
        description=transaction.description,
        date=transaction.date,
        created_at=transaction.created_at,
        updated_at=transaction.updated_at,
    )


def create_transaction(
        *,
        account_id: int,
        category_id: int,
        date: datetime.datetime,
        amount: Decimal,
        description: str | None,
) -> TransactionListItem:
    transaction = Transaction(
        account_id=account_id,
        category_id=category_id,
        date=date,
        amount=amount,
        description=description,
    )
    transaction.full_clean()
    transaction.save()

    return map_transaction_to_list_item(transaction)


def get_transactions_page(
        *,
        user_id: int,
        take: int = 1000,
        skip: int = 0,
        from_date: datetime.datetime | None = None,
        to_date: datetime.datetime | None = None,
        category_type: int | None = None,
) -> TransactionsPage:
    user_transactions = (
        Transaction.objects
        .filter(Q(account__user_id=user_id) | Q(category__user_id=user_id))
    )
    if from_date:
        user_transactions = user_transactions.filter(date__gte=from_date)
    if to_date:
        user_transactions = user_transactions.filter(date__lte=to_date)
    if category_type:
        user_transactions = user_transactions.filter(
            category__type=category_type
        )
    transactions_count = user_transactions.count()
    transactions = (
        user_transactions
        .select_related('category', 'account')
        .order_by('-date')
        [skip: skip + take]
    )

    transactions = [
        map_transaction_to_list_item(transaction)
        for transaction in transactions
    ]

    return TransactionsPage(
        transactions=transactions,
        pagination=Pagination(
            taken_count=take,
            skipped_count=skip,
            total_count=transactions_count,
        )
    )


def get_transaction(
        *,
        transaction_id: int,
        user_id: int,
) -> Transaction:
    try:
        transaction = (
            Transaction.objects
            .select_related('category', 'account')
            .get(id=transaction_id)
        )
    except Transaction.DoesNotExist:
        raise TransactionNotFoundError
    if (
            transaction.category.user_id != user_id
            or transaction.account.user_id != user_id
    ):
        raise TransactionAccessDeniedError
    return transaction


def delete_transaction_by_id(
        *,
        transaction_id: int,
        user_id: int,
) -> None:
    get_transaction(transaction_id=transaction_id, user_id=user_id).delete()


def update_transaction(
        *,
        transaction_id: int,
        user_id: int,
        date: datetime.datetime,
        amount: Decimal,
        description: str | None,
) -> None:
    transaction = get_transaction(
        transaction_id=transaction_id,
        user_id=user_id,
    )
    transaction.date = date
    transaction.amount = amount
    transaction.description = description
    transaction.save(
        update_fields=(
            'date',
            'amount',
            'description',
            'updated_at',
        )
    )
