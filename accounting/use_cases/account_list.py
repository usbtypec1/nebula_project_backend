from dataclasses import dataclass

from accounting.services.accounts import (
    AccountsWithBalanceDto,
    get_accounts_with_balance_by_user_id,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class AccountListUseCase:
    user_id: int

    def execute(self) -> AccountsWithBalanceDto:
        return get_accounts_with_balance_by_user_id(self.user_id)
