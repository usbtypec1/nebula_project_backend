from dataclasses import dataclass
from decimal import Decimal

from accounting.services.accounts import AccountCreateResultDto, create_account
from telegram_auth.services import ensure_user_exists


@dataclass(frozen=True, slots=True, kw_only=True)
class AccountCreateUseCase:
    name: str
    user_id: int
    is_public: bool
    initial_balance: Decimal

    def execute(self) -> AccountCreateResultDto:
        ensure_user_exists(self.user_id)
        return create_account(
            name=self.name,
            user_id=self.user_id,
            is_public=self.is_public,
            initial_balance=self.initial_balance,
        )
