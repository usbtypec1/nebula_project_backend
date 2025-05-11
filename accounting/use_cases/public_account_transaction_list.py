from dataclasses import dataclass

from accounting.exceptions import AccountAccessDeniedError
from accounting.services.accounts import get_account_by_id
from accounting.services.transactions import get_transactions_page


@dataclass(frozen=True, slots=True, kw_only=True)
class PublicAccountTransactionListUseCase:
    account_id: int

    def execute(self):
        account = get_account_by_id(self.account_id)
        if not account.is_public:
            raise AccountAccessDeniedError
        return get_transactions_page(account_ids=[self.account_id])
