import datetime
from dataclasses import dataclass
from decimal import Decimal

from accounting.services.transactions import update_transaction


@dataclass(frozen=True, slots=True, kw_only=True)
class TransactionUpdateUseCase:
    transaction_id: int
    user_id: int
    date: datetime.datetime
    amount: Decimal
    description: str | None

    def execute(self) -> None:
        update_transaction(
            transaction_id=self.transaction_id,
            user_id=self.user_id,
            date=self.date,
            amount=self.amount,
            description=self.description,
        )
