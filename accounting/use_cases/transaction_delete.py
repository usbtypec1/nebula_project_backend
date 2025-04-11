from dataclasses import dataclass

from accounting.services.transactions import delete_transaction_by_id


@dataclass(frozen=True, slots=True, kw_only=True)
class TransactionDeleteUseCase:
    user_id: int
    transaction_id: int

    def execute(self) -> None:
        delete_transaction_by_id(
            transaction_id=self.transaction_id,
            user_id=self.user_id,
        )
