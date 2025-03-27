from dataclasses import dataclass

from accounting.services.accounts import (
    ensure_user_has_access_to_account,
    get_account_with_balance_by_id,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class AccountRetrieveUseCase:
    account_id: int
    user_id: int

    def execute(self):
        account = get_account_with_balance_by_id(self.account_id)
        ensure_user_has_access_to_account(
            account=account,
            user_id=self.user_id,
        )
        return account
