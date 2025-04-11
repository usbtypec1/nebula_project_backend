from dataclasses import dataclass
from decimal import Decimal
import datetime

from django.db.models import Q

from accounting.models import Transfer
from accounting.exceptions import (
    TransferNotFoundError,
    TransferAccessDeniedError,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class Pagination:
    taken_count: int
    skipped_count: int
    total_count: int


@dataclass(frozen=True, slots=True, kw_only=True)
class TransferListItem:
    id: int
    from_account_id: int
    from_account_name: str
    to_account_id: int
    to_account_name: str
    amount: Decimal
    description: str | None
    date: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class TransfersPage:
    transfers: list[TransferListItem]
    pagination: Pagination


def map_transfer_to_list_item(
        transfer: Transfer,
) -> TransferListItem:
    return TransferListItem(
        id=transfer.id,
        from_account_id=transfer.from_account.id,
        from_account_name=transfer.from_account.name,
        to_account_id=transfer.to_account.id,
        to_account_name=transfer.to_account.name,
        amount=transfer.amount,
        description=transfer.description,
        date=transfer.date,
        created_at=transfer.created_at,
        updated_at=transfer.updated_at,
    )


def create_transfer(
        *,
        from_account_id: int,
        to_account_id: int,
        date: datetime.datetime,
        amount: Decimal,
        description: str | None,
) -> TransferListItem:
    transfer = Transfer(
        from_account_id=from_account_id,
        to_account_id=to_account_id,
        date=date,
        amount=amount,
        description=description,
    )
    transfer.full_clean()
    transfer.save()
    return map_transfer_to_list_item(transfer)


def get_transfers_page(
        *,
        user_id: int,
        take: int = 1000,
        skip: int = 0,
) -> TransfersPage:
    user_transfers = Transfer.objects.filter(
        Q(from_account__user_id=user_id) | Q(to_account__user_id=user_id)
    )
    transfers_count = user_transfers.count()
    transfers = (
        user_transfers
        .select_related('from_account', 'to_account')
        .order_by('-date')[skip:skip + take]
    )

    transfers = [
        map_transfer_to_list_item(transfer)
        for transfer in transfers
    ]

    return TransfersPage(
        transfers=transfers,
        pagination=Pagination(
            taken_count=take,
            skipped_count=skip,
            total_count=transfers_count,
        )
    )


def get_transfer(
        *,
        transfer_id: int,
        user_id: int,
) -> Transfer:
    try:
        transfer = Transfer.objects.select_related(
            'from_account', 'to_account'
        ).get(id=transfer_id)
    except Transfer.DoesNotExist:
        raise TransferNotFoundError
    if (
            transfer.from_account.user_id != user_id
            or transfer.to_account.user_id != user_id
    ):
        raise TransferAccessDeniedError
    return transfer


def delete_transfer_by_id(
        *,
        transfer_id: int,
        user_id: int,
) -> None:
    get_transfer(transfer_id=transfer_id, user_id=user_id).delete()


def update_transfer(
        *,
        transfer_id: int,
        user_id: int,
        date: datetime.datetime,
        amount: Decimal,
        description: str | None,
) -> None:
    transfer = get_transfer(
        transfer_id=transfer_id,
        user_id=user_id,
    )
    transfer.date = date
    transfer.amount = amount
    transfer.description = description
    transfer.save(
        update_fields=(
            'date',
            'amount',
            'description',
            'updated_at',
        )
    )
