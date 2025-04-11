import datetime
from dataclasses import dataclass
from decimal import Decimal

from accounting.services.transactions import (
    create_transaction,
    TransactionListItem,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class TransactionCreateUseCase:
    user_id: int
    account_id: int
    category_id: int
    date: datetime.datetime
    amount: Decimal
    description: str | None

    def execute(self) -> TransactionListItem:
        return create_transaction(
            account_id=self.account_id,
            category_id=self.category_id,
            date=self.date,
            amount=self.amount,
            description=self.description,
        )
