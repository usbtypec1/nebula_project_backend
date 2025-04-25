from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from exchange_rates.models import ExchangeRate


@pytest.mark.django_db
def test_exchange_rate_creation():
    now_time = timezone.now()

    rate = ExchangeRate.objects.create(
        currency_code=ExchangeRate.CurrencyCode.USD,
        rate=Decimal('83.50'),
        updated_at=now_time,
    )

    assert rate.currency_code == ExchangeRate.CurrencyCode.USD
    assert rate.rate == Decimal('83.50')
    assert rate.updated_at == now_time


@pytest.mark.django_db
def test_exchange_rate_currency_code_unique():
    ExchangeRate.objects.create(
        currency_code=ExchangeRate.CurrencyCode.USD,
        rate=Decimal('83.50'),
        updated_at=timezone.now(),
    )

    with pytest.raises(IntegrityError):
        ExchangeRate.objects.create(
            currency_code=ExchangeRate.CurrencyCode.USD,
            rate=Decimal('84.20'),
            updated_at=timezone.now(),
        )


def test_valid_currency_codes():
    valid_codes = {choice[0] for choice in ExchangeRate.CurrencyCode.choices}
    expected_codes = {'usd', 'eur', 'rub', 'kzt'}
    assert valid_codes == expected_codes


@pytest.mark.django_db
def test_exchange_rate_update():
    rate = ExchangeRate.objects.create(
        currency_code=ExchangeRate.CurrencyCode.EUR,
        rate=Decimal('90.75'),
        updated_at=timezone.now(),
    )

    new_rate = Decimal('91.20')
    new_time = timezone.now()
    rate.rate = new_rate
    rate.updated_at = new_time
    rate.save()

    updated_rate = ExchangeRate.objects.get(pk=rate.pk)
    assert updated_rate.rate == new_rate
    assert updated_rate.updated_at == new_time


@pytest.mark.django_db
def test_exchange_rate_max_digits():
    large_rate = Decimal('99999999.99')  # 10 цифр, 2 после запятой

    rate = ExchangeRate(
        currency_code=ExchangeRate.CurrencyCode.RUB,
        rate=large_rate,
        updated_at=timezone.now(),
    )

    rate.full_clean()
    rate.save()

    too_large_rate = Decimal('999999999.99')  # 11 цифр, 2 после запятой

    rate.rate = too_large_rate
    with pytest.raises(ValidationError):
        rate.full_clean()


@pytest.mark.django_db
def test_exchange_rate_str_representation():
    rate = ExchangeRate.objects.create(
        currency_code=ExchangeRate.CurrencyCode.USD,
        rate=Decimal('83.50'),
        updated_at=timezone.now(),
    )

    # __str__ не определен в модели, поэтому используем стандартное представление
    expected_str = "ExchangeRate object (1)"
    assert str(rate) == expected_str


def test_exchange_rate_meta_verbose_names():
    assert ExchangeRate._meta.verbose_name == 'Exchange Rate'
    assert ExchangeRate._meta.verbose_name_plural == 'Exchange Rates'
