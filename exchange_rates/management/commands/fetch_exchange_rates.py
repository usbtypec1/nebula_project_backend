from django.core.management import BaseCommand

from exchange_rates.use_cases import ExchangeRatesFetchAndUpdateUseCase


class Command(BaseCommand):

    def handle(self, *args, **options):
        ExchangeRatesFetchAndUpdateUseCase().execute()
        self.stdout.write(
            self.style.SUCCESS('Successfully fetched exchange rates'),
        )
