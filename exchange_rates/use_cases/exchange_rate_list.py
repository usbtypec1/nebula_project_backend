from dataclasses import dataclass

from exchange_rates.models import ExchangeRate
from exchange_rates.services.akchabar import AkchabarExchangeRateDto


@dataclass(frozen=True, slots=True, kw_only=True)
class ExchangeRateListUseCase:

    def execute(self) -> list[AkchabarExchangeRateDto]:
        exchange_rates = ExchangeRate.objects.all()
        return [
            AkchabarExchangeRateDto(
                rate=exchange_rate.rate,
                currency_code=ExchangeRate.CurrencyCode(
                    exchange_rate.currency_code
                ),
                updated_at=exchange_rate.updated_at,
            )
            for exchange_rate in exchange_rates
        ]
