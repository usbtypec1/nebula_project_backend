import pytest
from decimal import Decimal

from exchange_rates.models import ExchangeRate
from exchange_rates.services.akchabar import AkchabarExchangeRateDto
from exchange_rates.tests.factories import ExchangeRateFactory
from exchange_rates.use_cases.exchange_rate_list import ExchangeRateListUseCase


@pytest.mark.django_db
def test_empty_exchange_rate_list():
    # Arrange - база данных пуста

    result = ExchangeRateListUseCase().execute()

    assert result == []

@pytest.mark.django_db
def test_single_exchange_rate():
    usd_rate = ExchangeRateFactory(
        currency_code=ExchangeRate.CurrencyCode.USD,
        rate=Decimal('89.50'),
    )

    result = ExchangeRateListUseCase().execute()

    assert len(result) == 1

    actual_dto = result[0]
    assert actual_dto.currency_code == ExchangeRate.CurrencyCode.USD
    assert actual_dto.rate == usd_rate.rate
    assert actual_dto.updated_at == usd_rate.updated_at

@pytest.mark.django_db
def test_multiple_exchange_rates_three():
    rub_rate = ExchangeRateFactory(
        currency_code=ExchangeRate.CurrencyCode.RUB,
        rate=Decimal('1.05'),
    )
    usd_rate = ExchangeRateFactory(
        currency_code=ExchangeRate.CurrencyCode.USD,
        rate=Decimal('87.50'),
    )
    eur_rate = ExchangeRateFactory(
        currency_code=ExchangeRate.CurrencyCode.EUR,
        rate=Decimal('99.95'),
    )

    result = ExchangeRateListUseCase().execute()

    assert len(result) == 3

    result_codes = {dto.currency_code for dto in result}
    assert ExchangeRate.CurrencyCode.RUB in result_codes
    assert ExchangeRate.CurrencyCode.USD in result_codes
    assert ExchangeRate.CurrencyCode.EUR in result_codes

    assert any(dto.rate == rub_rate.rate and dto.currency_code == rub_rate.currency_code for dto in result)
    assert any(dto.rate == usd_rate.rate and dto.currency_code == usd_rate.currency_code for dto in result)
    assert any(dto.rate == eur_rate.rate and dto.currency_code == eur_rate.currency_code for dto in result)


@pytest.mark.django_db
def test_multiple_exchange_rates_dto_fields():
    usd_rate = ExchangeRateFactory(
        currency_code=ExchangeRate.CurrencyCode.USD,
        rate=Decimal('89.50'),
    )

    eur_rate = ExchangeRateFactory(
        currency_code=ExchangeRate.CurrencyCode.EUR,
        rate=Decimal('95.75'),
    )

    result = ExchangeRateListUseCase().execute()

    assert len(result) == 2

    expected_dtos = {
        ExchangeRate.CurrencyCode.USD: AkchabarExchangeRateDto(
            currency_code=ExchangeRate.CurrencyCode.USD,
            rate=usd_rate.rate,
            updated_at=usd_rate.updated_at,
        ),
        ExchangeRate.CurrencyCode.EUR: AkchabarExchangeRateDto(
            currency_code=ExchangeRate.CurrencyCode.EUR,
            rate=eur_rate.rate,
            updated_at=eur_rate.updated_at,
        )
    }

    result_dict = {dto.currency_code: dto for dto in result}

    for currency_code, expected_dto in expected_dtos.items():
        assert currency_code in result_dict
        actual_dto = result_dict[currency_code]
        assert actual_dto.rate == expected_dto.rate
        assert actual_dto.currency_code == expected_dto.currency_code
        assert actual_dto.updated_at == expected_dto.updated_at


@pytest.mark.django_db
def test_currency_code_enum_conversion():
    usd_rate = ExchangeRateFactory(
        currency_code=ExchangeRate.CurrencyCode.USD,
        rate=Decimal('89.50'),
    )

    result = ExchangeRateListUseCase().execute()

    assert len(result) == 1

    actual_dto = result[0]

    assert isinstance(actual_dto.currency_code, ExchangeRate.CurrencyCode)
    assert actual_dto.currency_code == ExchangeRate.CurrencyCode.USD