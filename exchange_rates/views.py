from django.shortcuts import render
from dataclasses import asdict
from django.http import JsonResponse
from exchange_rates.services import rates_parser
from exchange_rates.models import BaseExchangeRateData, ExchangeRateData
from typing import Iterable
# Create your views here.

def get_rates(requests):
    rateItems: Iterable[ExchangeRateData] = rates_parser()
    data = []

    for item in rateItems:
        rate_dict = asdict(item)
        data.append(rate_dict)

        BaseExchangeRateData.objects.update_or_create(
            bank_name=item.bank_name,
            currency_code=item.currency_code,
            defaults={
                "buy_rate": rate_dict["buy_rate"],
                "sell_rate": rate_dict["sell_rate"],
                "updated_at": rate_dict["updated_at"],
            }
        )

    return JsonResponse(data, safe=False)
