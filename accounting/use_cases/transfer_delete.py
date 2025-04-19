from dataclasses import dataclass

from accounting.services.transfers import delete_transfer_by_id


@dataclass(frozen=True, slots=True, kw_only=True)
class TransferDeleteUseCase:
    transfer_id: int
    user_id: int

    def execute(self) -> None:
        delete_transfer_by_id(
            transfer_id=self.transfer_id,
            user_id=self.user_id,
        )
