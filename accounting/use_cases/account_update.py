from dataclasses import dataclass
from decimal import Decimal

from accounting.services.accounts import (
    ensure_user_has_access_to_account, get_account_by_id,
    update_account_by_id,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class AccountUpdateUseCase:
    account_id: int
    user_id: int
    name: str
    is_public: bool
    initial_balance: Decimal

    def execute(self) -> None:
        account = get_account_by_id(self.account_id)
        ensure_user_has_access_to_account(
            user_id=self.user_id,
            account=account,
        )
        update_account_by_id(
            account_id=self.account_id,
            name=self.name,
            is_public=self.is_public,
            initial_balance=self.initial_balance,
        )
