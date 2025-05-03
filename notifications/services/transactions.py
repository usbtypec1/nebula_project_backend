import datetime
import logging
from abc import abstractmethod
from dataclasses import dataclass
from typing import override, Protocol

from django.conf import settings
from django.db.models import Max
from django.utils import timezone
from telebot import TeleBot

from telegram_auth.models import User


log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class UserWithoutRecentTransactions:
    user_id: int
    last_transaction_at: datetime.datetime

    @property
    def transactions_gap_days(self) -> int:
        """
        Calculate the number of days since the last transaction.
        """
        return (timezone.now() - self.last_transaction_at).days


def get_users_without_recent_transactions(
        days_threshold: int,
) -> list[UserWithoutRecentTransactions]:
    """
    Get users who have not made any transactions in the last
    `days_threshold` days,
    but made at least one transaction before that.
    """
    cutoff_date = timezone.now() - datetime.timedelta(days=days_threshold)
    return (
        User.objects
        .annotate(last_transaction_at=Max('accounts__transactions__date'))
        .filter(
            last_transaction_at__lt=cutoff_date,
            notification_settings__transactions_gap=True,
        )
        .distinct()
    )


class Message(Protocol):

    @abstractmethod
    def get_text(self) -> str: ...


@dataclass(frozen=True, slots=True, kw_only=True)
class MissingRecentTransactionsMessage(Message):
    transactions_gap_days: int

    @override
    def get_text(self) -> str:
        return (
            f"Вы не делали записей уже {self.transactions_gap_days} дней 😔.\n"
            "Начните прямо сейчас 🔥"
        )


def send_message(chat_id: int, message: Message) -> None:
    bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)
    try:
        bot.send_message(chat_id=chat_id, text=message.get_text())
    except Exception as error:
        log.error("Could not send message to Telegram: %s", error)
    else:
        log.info("Message sent to user %s", chat_id)
