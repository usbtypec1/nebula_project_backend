from exchange_rates.services.exchange_rates import upsert_exchange_rates
from exchange_rates.services.valutakg import (
    create_valuta_kg_http_client,
    ValutaKgGateway,
)


class ExchangeRatesFetchAndUpdateUseCase:

    def execute(self) -> None:
        with create_valuta_kg_http_client() as http_client:
            gateway = ValutaKgGateway(http_client=http_client)
            exchange_rates = gateway.get_exchange_rates()
        upsert_exchange_rates(exchange_rates)
