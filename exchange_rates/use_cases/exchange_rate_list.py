from dataclasses import dataclass

from exchange_rates.models import ExchangeRate
from exchange_rates.services.valutakg import ExchangeRateDto


@dataclass(frozen=True, slots=True, kw_only=True)
class ExchangeRateListUseCase:

    def execute(self) -> list[ExchangeRateDto]:
        exchange_rates = ExchangeRate.objects.all()
        return [
            ExchangeRateDto(
                source_name=exchange_rate.source_name,
                logo_url=exchange_rate.logo_url,
                buy_rate=exchange_rate.buy_rate,
                sell_rate=exchange_rate.sell_rate,
                currency_code=ExchangeRate.CurrencyCode(
                    exchange_rate.currency_code
                ),
                updated_at=exchange_rate.updated_at,
            )
            for exchange_rate in exchange_rates
        ]
