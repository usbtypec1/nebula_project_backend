from dataclasses import dataclass

from notifications.services.transactions import (
    get_users_without_recent_transactions,
    MissingRecentTransactionsMessage,
    send_message,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class MissingTransactionsNotificationsUseCase:
    days_threshold: int

    def execute(self):
        users = get_users_without_recent_transactions(self.days_threshold)

        for user in users:
            message = MissingRecentTransactionsMessage(
                transactions_gap_days=user.transactions_gap_days,
            )
            send_message(chat_id=user.user_id, message=message)
