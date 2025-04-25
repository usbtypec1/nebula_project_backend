import factory
from django.utils.timezone import now
from decimal import Decimal

from faker.generator import random

from exchange_rates.models import ExchangeRate


class ExchangeRateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExchangeRate

    currency_code = factory.Iterator([
        ExchangeRate.CurrencyCode.USD,
        ExchangeRate.CurrencyCode.EUR,
        ExchangeRate.CurrencyCode.RUB,
        ExchangeRate.CurrencyCode.KZT,
    ])
    # rate = factory.LazyFunction(lambda: Decimal('1.00') + Decimal(str(factory.random.randgen.random() * 100)).quantize(Decimal('0.01')))
    rate = factory.LazyFunction(lambda: Decimal(f"{random.uniform(1, 100):.2f}"))
    updated_at = factory.LazyFunction(now)