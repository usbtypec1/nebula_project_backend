from exchange_rates.services.akchabar import (
    AkchabarGateway, create_akchabar_gateway_http_client,
)
from exchange_rates.services.exchange_rates import upsert_exchange_rates


class ExchangeRatesFetchAndUpdateUseCase:

    def execute(self) -> None:
        with create_akchabar_gateway_http_client() as http_client:
            gateway = AkchabarGateway(http_client=http_client)
            exchange_rates = gateway.get_national_bank_exchange_rates()
        upsert_exchange_rates(exchange_rates)
