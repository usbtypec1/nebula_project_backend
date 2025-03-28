import httpx
from bs4 import BeautifulSoup
from exchange_rates.models import ExchangeRateData
from typing import Iterable

def rates_parser() -> Iterable[ExchangeRateData]:
    response = httpx.get("https://valuta.kg/")
    soup = BeautifulSoup(response.text, 'lxml')
    rows = soup.select(".rate-list.active tr")
    res = []

    for row in rows[1:-1]:
        type = row.select_one(".min-width-80").get_text(strip=True)
        bank_name = row.select_one("a").get_text(strip=True)
        usd_buy_rate = row.select_one(".td-rate--even:nth-child(2) .td-rate__wrp").get_text(strip=True)
        eur_buy_rate = row.select_one(".td-rate:nth-child(4) .td-rate__wrp").get_text(strip=True)
        rub_buy_rate = row.select_one(".-last-in-group+ .td-rate--even .td-rate__wrp").get_text(strip=True)
        kzt_buy_rate = row.select_one(".td-rate:nth-child(8) .td-rate__wrp").get_text(strip=True)
        usd_sell_rate = row.select_one(".-last-in-group:nth-child(3) .td-rate__wrp").get_text(strip=True)
        eur_sell_rate = row.select_one(".-last-in-group:nth-child(5) .td-rate__wrp").get_text(strip=True)
        rub_sell_rate = row.select_one(".-last-in-group~ .td-rate--even.-last-in-group .td-rate__wrp").get_text(strip=True)
        kzt_sell_rate = row.select_one(".-last-in-group:nth-child(9) .td-rate__wrp").get_text(strip=True)

        if type == "Банк":
            usdRate = ExchangeRateData(
                bank_name=bank_name, sell_rate=float(usd_sell_rate),
                buy_rate=float(usd_buy_rate), currency_code="USD",
            )
            eurRate = ExchangeRateData(
                bank_name=bank_name, sell_rate=float(eur_sell_rate),
                buy_rate=float(eur_buy_rate), currency_code="EUR"
            )
            kztRate = ExchangeRateData(
                bank_name=bank_name, sell_rate=float(kzt_sell_rate),
                buy_rate=float(kzt_buy_rate), currency_code="KZT"
            )
            rubRate = ExchangeRateData(
                bank_name=bank_name, sell_rate=float(rub_sell_rate),
                buy_rate=float(rub_buy_rate), currency_code="RU"
            )
            res.extend([usdRate, eurRate, kztRate, rubRate])
    return res