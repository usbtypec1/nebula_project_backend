from dataclasses import dataclass

from accounting.services.accounts import (
    delete_account_by_id,
    ensure_user_has_access_to_account,
    get_account_by_id,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class AccountDeleteUseCase:
    account_id: int
    user_id: int

    def execute(self) -> None:
        account = get_account_by_id(self.account_id)
        ensure_user_has_access_to_account(
            user_id=self.user_id,
            account=account,
        )
        delete_account_by_id(account.id)
