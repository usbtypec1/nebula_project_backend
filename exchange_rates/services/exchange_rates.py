from collections.abc import Iterable

from exchange_rates.models import ExchangeRate
from exchange_rates.services.valutakg import ExchangeRateDto


def upsert_exchange_rates(exchange_rates: Iterable[ExchangeRateDto]) -> None:
    for exchange_rate in exchange_rates:
        ExchangeRate.objects.update_or_create(
            source_name=exchange_rate.source_name,
            currency_code=exchange_rate.currency_code,
            defaults={
                'logo_url': exchange_rate.logo_url,
                'buy_rate': exchange_rate.buy_rate,
                'sell_rate': exchange_rate.sell_rate,
                'updated_at': exchange_rate.updated_at,
            }
        )
