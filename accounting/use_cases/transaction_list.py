import datetime
from dataclasses import dataclass

from accounting.services.transactions import (
    get_transactions_page,
    TransactionsPage,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class TransactionListUseCase:
    user_id: int
    take: int
    skip: int
    from_date: datetime.datetime | None = None
    to_date: datetime.datetime | None = None
    category_type: int | None = None

    def execute(self) -> TransactionsPage:
        return get_transactions_page(
            user_id=self.user_id,
            take=self.take,
            skip=self.skip,
        )
