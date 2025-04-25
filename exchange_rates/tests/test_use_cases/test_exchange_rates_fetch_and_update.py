import datetime
from decimal import Decimal
from unittest.mock import patch
from zoneinfo import ZoneInfo

import pytest

from exchange_rates.models import ExchangeRate
from exchange_rates.use_cases.exchange_rates_fetch_and_update import ExchangeRatesFetchAndUpdateUseCase


@pytest.mark.django_db
def test_exchange_rates_created(execute_use_case):
    exchange_rates = list(ExchangeRate.objects.all())
    assert len(exchange_rates) == 2


@pytest.mark.django_db
def test_usd_rate_data_correct(execute_use_case, expected_datetime):
    usd = ExchangeRate.objects.get(currency_code='usd')
    assert usd.rate == Decimal('87.50')
    assert usd.updated_at == expected_datetime


@pytest.mark.django_db
def test_usd_rate_data_correct(execute_use_case, expected_datetime):
    usd = ExchangeRate.objects.get(currency_code='usd')
    assert usd.rate == Decimal('87.50')
    assert usd.updated_at == expected_datetime


@pytest.mark.django_db
def test_exchange_rates_count_after_update(
    existing_usd_rate,
    execute_update_use_case
):
    exchange_rates = list(ExchangeRate.objects.all())
    assert len(exchange_rates) == 2


@pytest.mark.django_db
def test_usd_rate_is_updated(
    existing_usd_rate,
    execute_update_use_case,
    expected_updated_datetime
):
    existing_usd_rate.refresh_from_db()
    assert existing_usd_rate.rate == Decimal('87.50')
    assert existing_usd_rate.updated_at == expected_updated_datetime


@pytest.mark.django_db
def test_rub_rate_is_created(
    execute_update_use_case,
    expected_updated_datetime
):
    rub = ExchangeRate.objects.get(currency_code=ExchangeRate.CurrencyCode.RUB)
    assert rub.rate == Decimal('0.97')
    assert rub.updated_at == expected_updated_datetime


@pytest.mark.django_db
def test_empty_response_does_not_crash():
    with patch('exchange_rates.services.akchabar.AkchabarGatewayHttpClient') as MockHttpClient:
        mock_client = MockHttpClient.return_value
        mock_client.get.return_value.json.return_value = {
            'date': '19.04.2025',
            'time': '19:00:00',
            'rate_values': []
        }
        with patch('exchange_rates.services.akchabar.create_akchabar_gateway_http_client', return_value=mock_client):
            ExchangeRatesFetchAndUpdateUseCase().execute()
    assert ExchangeRate.objects.count() == 0


@pytest.mark.django_db
def test_old_currency_not_deleted_after_update(existing_usd_rate, execute_update_use_case):
    assert ExchangeRate.objects.filter(currency_code='usd').exists()


@pytest.mark.django_db
def test_new_currency_created_correctly(execute_update_use_case):
    rub = ExchangeRate.objects.get(currency_code='rub')
    assert rub.rate == Decimal('0.97')


@pytest.mark.django_db
def test_invalid_rate_format_raises_exception():
    mock_data = {
        'date': '19.04.2025',
        'time': '19:00:00',
        'rate_values': [{'currency': 'usd', 'buy_rate': 'not_a_number'}]
    }

    with patch('exchange_rates.services.akchabar.AkchabarGatewayHttpClient') as MockHttpClient:
        mock_client = MockHttpClient.return_value
        mock_client.get.return_value.json.return_value = mock_data
        with patch('exchange_rates.services.akchabar.create_akchabar_gateway_http_client', return_value=mock_client):
            with pytest.raises(Exception):
                ExchangeRatesFetchAndUpdateUseCase().execute()


@pytest.mark.django_db
def test_duplicate_currency_last_one_wins():
    mock_data = {
        'date': '19.04.2025',
        'time': '19:00:00',
        'rate_values': [
            {'currency': 'usd', 'buy_rate': '86.00'},
            {'currency': 'usd', 'buy_rate': '88.00'}
        ]
    }

    with patch('exchange_rates.services.akchabar.AkchabarGatewayHttpClient') as MockHttpClient:
        mock_client = MockHttpClient.return_value
        mock_client.get.return_value.json.return_value = mock_data
        with patch('exchange_rates.services.akchabar.create_akchabar_gateway_http_client', return_value=mock_client):
            ExchangeRatesFetchAndUpdateUseCase().execute()

    usd = ExchangeRate.objects.get(currency_code='usd')
    assert usd.rate == Decimal('88.00')