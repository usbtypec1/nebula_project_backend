from django.core.management import BaseCommand

from notifications.use_cases.missing_transactions import (
    MissingTransactionsNotificationsUseCase
)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--days_threshold',
            type=int,
            help='Number of days threshold for notifications',
            default=3,
            required=False,
        )

    def handle(self, *args, **options):
        days_threshold = options['days_threshold']
        MissingTransactionsNotificationsUseCase(days_threshold=days_threshold)
