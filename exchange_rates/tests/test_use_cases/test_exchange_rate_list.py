import pytest
from decimal import Decimal

from exchange_rates.models import ExchangeRate
from exchange_rates.services.akchabar import AkchabarExchangeRateDto
from exchange_rates.tests.factories import ExchangeRateFactory
from exchange_rates.use_cases.exchange_rate_list import ExchangeRateListUseCase


@pytest.mark.django_db
def test_exchange_rate_list_returns_dto_list():
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
def test_exchange_rate_list_returns_empty_list_when_no_rates():
    # Arrange - база данных пуста

    result = ExchangeRateListUseCase().execute()

    assert result == []