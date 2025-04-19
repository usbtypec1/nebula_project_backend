import datetime
from dataclasses import dataclass
from decimal import Decimal

from accounting.services.transfers import create_transfer, TransferListItem


@dataclass(frozen=True, slots=True, kw_only=True)
class TransferCreateUseCase:
    from_account_id: int
    to_account_id: int
    date: datetime.datetime
    amount: Decimal
    description: str | None

    def execute(self) -> TransferListItem:
        return create_transfer(
            from_account_id=self.from_account_id,
            to_account_id=self.to_account_id,
            date=self.date,
            amount=self.amount,
            description=self.description,
        )
