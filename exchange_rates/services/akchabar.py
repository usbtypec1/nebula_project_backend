import contextlib
import datetime
from collections.abc import Generator
from dataclasses import dataclass
from decimal import Decimal
from typing import NewType
from zoneinfo import ZoneInfo

import httpx
from fake_useragent import UserAgent


ua = UserAgent()

AkchabarGatewayHttpClient = NewType(
    'AkchabarGatewayHttpClient',
    httpx.Client,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class AkchabarExchangeRateDto:
    currency_code: str
    rate: Decimal
    updated_at: datetime.datetime


@contextlib.contextmanager
def create_akchabar_gateway_http_client(
        *,
        timeout: int | float | None = 5,
) -> Generator[AkchabarGatewayHttpClient, None, None]:
    with httpx.Client(
            base_url="https://www.akchabar.kg/",
            headers={'User-Agent': ua.random},
            timeout=timeout,
    ) as http_client:
        yield AkchabarGatewayHttpClient(http_client)


@dataclass(frozen=True, slots=True, kw_only=True)
class AkchabarGateway:
    http_client: AkchabarGatewayHttpClient

    def get_national_bank_exchange_rates(
            self,
    ) -> list[AkchabarExchangeRateDto]:
        url = "/api/v2/rates/nbkr/current/"
        response = self.http_client.get(url)
        response_data = response.json()
        date: str = response_data['date']
        time: str = response_data['time']

        date: datetime.datetime = datetime.datetime.strptime(date, "%d.%m.%Y")
        time: datetime.time = datetime.time.fromisoformat(time)

        updated_at = datetime.datetime.combine(
            date=date,
            time=time,
            tzinfo=ZoneInfo("Asia/Bishkek"),
        )

        exchange_rates: list[AkchabarExchangeRateDto] = []
        for exchange_rate in response_data['rate_values']:
            currency_code: str = exchange_rate['currency']
            rate: Decimal = Decimal(exchange_rate['buy_rate'])

            exchange_rate = AkchabarExchangeRateDto(
                currency_code=currency_code,
                rate=rate,
                updated_at=updated_at,
            )
            exchange_rates.append(exchange_rate)

        return exchange_rates
