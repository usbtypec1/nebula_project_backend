from dataclasses import dataclass

from accounting.services.transfers import get_transfers_page, TransfersPage


@dataclass(frozen=True, slots=True, kw_only=True)
class TransferListUseCase:
    user_id: int
    take: int
    skip: int

    def execute(self) -> TransfersPage:
        return get_transfers_page(
            user_id=self.user_id,
            take=self.take,
            skip=self.skip,
        )
