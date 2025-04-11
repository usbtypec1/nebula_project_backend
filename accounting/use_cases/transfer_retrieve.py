from dataclasses import dataclass

from accounting.services.transfers import (
    get_transfer,
    map_transfer_to_list_item,
    TransferListItem,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class TransferRetrieveUseCase:
    transfer_id: int
    user_id: int

    def execute(self) -> TransferListItem:
        return map_transfer_to_list_item(
            transfer=get_transfer(
                transfer_id=self.transfer_id,
                user_id=self.user_id,
            ),
        )
