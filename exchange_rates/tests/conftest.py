from decimal import Decimal

import pytest
import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

from exchange_rates.models import ExchangeRate
from exchange_rates.use_cases import ExchangeRatesFetchAndUpdateUseCase


@pytest.fixture
def mock_akchabar_response():
    return {
        'date': '19.04.2025',
        'time': '19:00:00',
        'rate_values': [
            {'currency': 'usd', 'buy_rate': '87.50'},
            {'currency': 'eur', 'buy_rate': '99.75'},
        ]
    }


@pytest.fixture
def expected_datetime():
    return datetime.datetime.combine(
        date=datetime.datetime.strptime('19.04.2025', '%d.%m.%Y'),
        time=datetime.time.fromisoformat('19:00:00'),
        tzinfo=ZoneInfo("Asia/Bishkek"),
    )


@pytest.fixture
def execute_use_case(mock_akchabar_response):
    with patch('exchange_rates.services.akchabar.AkchabarGatewayHttpClient') as MockHttpClient:
        mock_client_instance = MockHttpClient.return_value
        mock_response = mock_client_instance.get.return_value
        mock_response.json.return_value = mock_akchabar_response

        with patch('exchange_rates.services.akchabar.create_akchabar_gateway_http_client',
                   return_value=mock_client_instance):
            ExchangeRatesFetchAndUpdateUseCase().execute()

@pytest.fixture
def old_datetime():
    return datetime.datetime.now(tz=ZoneInfo("Asia/Bishkek"))


@pytest.fixture
def existing_usd_rate(old_datetime):
    return ExchangeRate.objects.create(
        currency_code=ExchangeRate.CurrencyCode.USD,
        rate=Decimal('85.25'),
        updated_at=old_datetime,
    )


@pytest.fixture
def mock_update_response():
    return {
        'date': '19.04.2025',
        'time': '19:45:00',
        'rate_values': [
            {'currency': 'usd', 'buy_rate': '87.50'},
            {'currency': 'rub', 'buy_rate': '0.97'},
        ]
    }


@pytest.fixture
def expected_updated_datetime():
    return datetime.datetime.combine(
        date=datetime.datetime.strptime('19.04.2025', '%d.%m.%Y'),
        time=datetime.time.fromisoformat('19:45:00'),
        tzinfo=ZoneInfo("Asia/Bishkek"),
    )


@pytest.fixture
def execute_update_use_case(mock_update_response):
    with patch('exchange_rates.services.akchabar.AkchabarGatewayHttpClient') as MockHttpClient:
        mock_client_instance = MockHttpClient.return_value
        mock_response = mock_client_instance.get.return_value
        mock_response.json.return_value = mock_update_response

        with patch('exchange_rates.services.akchabar.create_akchabar_gateway_http_client',
                   return_value=mock_client_instance):
            ExchangeRatesFetchAndUpdateUseCase().execute()
