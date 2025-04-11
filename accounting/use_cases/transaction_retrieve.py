from dataclasses import dataclass

from accounting.services.transactions import (
    get_transaction,
    map_transaction_to_list_item,
    TransactionListItem,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class TransactionRetrieveUseCase:
    transaction_id: int
    user_id: int

    def execute(self) -> TransactionListItem:
        return map_transaction_to_list_item(
            transaction=get_transaction(
                transaction_id=self.transaction_id,
                user_id=self.user_id,
            ),
        )
