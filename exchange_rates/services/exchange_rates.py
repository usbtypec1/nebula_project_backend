from collections.abc import Iterable

from exchange_rates.models import ExchangeRate
from exchange_rates.services.akchabar import AkchabarExchangeRateDto


def upsert_exchange_rates(
        exchange_rates: Iterable[AkchabarExchangeRateDto],
) -> None:
    for exchange_rate in exchange_rates:
        ExchangeRate.objects.update_or_create(
            currency_code=exchange_rate.currency_code,
            defaults={
                'rate': exchange_rate.rate,
                'updated_at': exchange_rate.updated_at,
            }
        )
