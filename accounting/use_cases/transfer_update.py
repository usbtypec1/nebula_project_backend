import datetime
from dataclasses import dataclass
from decimal import Decimal

from accounting.services.transfers import update_transfer


@dataclass(frozen=True, slots=True, kw_only=True)
class TransferUpdateUseCase:
    transfer_id: int
    user_id: int
    date: datetime.datetime
    description: str | None
    amount: Decimal

    def execute(self) -> None:
        update_transfer(
            transfer_id=self.transfer_id,
            user_id=self.user_id,
            date=self.date,
            description=self.description,
            amount=self.amount,
        )
