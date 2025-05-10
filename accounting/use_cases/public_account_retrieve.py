from dataclasses import dataclass

from accounting.exceptions import AccountAccessDeniedError
from accounting.services.accounts import get_account_with_balance_by_id


@dataclass(frozen=True, slots=True, kw_only=True)
class PublicAccountRetrieveUseCase:
    account_id: int

    def execute(self):
        account = get_account_with_balance_by_id(self.account_id)
        if not account.is_public:
            raise AccountAccessDeniedError
        return account
