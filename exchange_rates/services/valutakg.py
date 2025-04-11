import contextlib
import datetime
from collections.abc import Generator
from dataclasses import dataclass
from decimal import Decimal
from typing import NewType

import httpx
from bs4 import BeautifulSoup
from django.conf import settings
from django.utils import timezone
from fake_useragent import UserAgent

from exchange_rates.models import ExchangeRate


ua = UserAgent()

ValutaKgHttpClient = NewType('ValutaKgHttpClient', httpx.Client)


@dataclass(frozen=True, slots=True, kw_only=True)
class ExchangeRateDto:
    source_name: str
    logo_url: str | None
    buy_rate: Decimal
    sell_rate: Decimal
    currency_code: ExchangeRate.CurrencyCode
    updated_at: datetime.datetime


@contextlib.contextmanager
def create_valuta_kg_http_client(
        *,
        timeout: int | float | None = 5,
) -> Generator[ValutaKgHttpClient, None, None]:
    with httpx.Client(
            base_url="https://valuta.kg",
            headers={'User-Agent': ua.random},
            timeout=timeout,
    ) as http_client:
        yield ValutaKgHttpClient(http_client)


def parse_valuta_kg_exchange_rates_page_response(
        response: httpx.Response
) -> list[ExchangeRateDto]:
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    with open('response.html', 'w', encoding='utf-8') as file:
        file.write(response.text)

    table_body = soup.find('div', attrs={'class': ['rate-list', 'active']})
    if table_body is None:
        raise ValueError("Expected a table body")

    exchange_rates: list[ExchangeRateDto] = []

    rows = table_body.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        if len(tds) != 10:
            continue

        source_info_td = tds[0]

        img = source_info_td.find('img')
        if img is None:
            logo_url = None
        else:
            logo_url = img.get('src')

        print(logo_url)
        if not logo_url:
            logo_url = f'https:{logo_url}'

        source_name = source_info_td.find('h4')
        if source_name is None:
            source_name = None
        else:
            source_name = source_name.text

        if source_name is None:
            continue

        usd_buy_rate = tds[1].text.strip()
        usd_sell_rate = tds[2].text.strip()

        eur_buy_rate = tds[3].text.strip()
        eur_sell_rate = tds[4].text.strip()

        rub_buy_rate = tds[5].text.strip()
        rub_sell_rate = tds[6].text.strip()

        kzt_buy_rate = tds[7].text.strip()
        kzt_sell_rate = tds[8].text.strip()

        update_time = tds[9].text.strip()

        data = (
            (usd_buy_rate, usd_sell_rate, ExchangeRate.CurrencyCode.USD),
            (eur_buy_rate, eur_sell_rate, ExchangeRate.CurrencyCode.EUR),
            (rub_buy_rate, rub_sell_rate, ExchangeRate.CurrencyCode.RUB),
            (kzt_buy_rate, kzt_sell_rate, ExchangeRate.CurrencyCode.KZT),
        )
        for buy_rate, sell_rate, currency_code in data:
            updated_at = datetime.datetime.combine(
                timezone.now(),
                datetime.time.fromisoformat(update_time),
                tzinfo=settings.TIME_ZONE,
            )
            exchange_rates.append(
                ExchangeRateDto(
                    source_name=source_name,
                    logo_url=logo_url,
                    buy_rate=Decimal(buy_rate),
                    sell_rate=Decimal(sell_rate),
                    currency_code=currency_code,
                    updated_at=updated_at,
                )
            )

    return exchange_rates


@dataclass(frozen=True, slots=True, kw_only=True)
class ValutaKgGateway:
    http_client: ValutaKgHttpClient

    def request_exchange_rates_page(self) -> httpx.Response:
        return self.http_client.get('/')

    def get_exchange_rates(self) -> list[ExchangeRateDto]:
        response = self.request_exchange_rates_page()
        return parse_valuta_kg_exchange_rates_page_response(response)
