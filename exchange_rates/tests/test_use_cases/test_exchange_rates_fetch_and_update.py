import datetime
from decimal import Decimal
from unittest.mock import patch
from zoneinfo import ZoneInfo

import pytest

from exchange_rates.models import ExchangeRate
from exchange_rates.use_cases.exchange_rates_fetch_and_update import ExchangeRatesFetchAndUpdateUseCase


@pytest.mark.django_db
def test_exchange_rates_fetch_and_update_creates_new_rates():
    mock_response_data = {
        'date': '19.04.2025',
        'time': '19:00:00',
        'rate_values': [
            {'currency': 'usd', 'buy_rate': '87.50'},
            {'currency': 'eur', 'buy_rate': '99.75'},
        ]
    }

    expected_datetime = datetime.datetime.combine(
        date=datetime.datetime.strptime('19.04.2025', '%d.%m.%Y'),
        time=datetime.time.fromisoformat('19:00:00'),
        tzinfo=ZoneInfo("Asia/Bishkek"),
    )

    # Мокаем ответ HTTP клиента
    with patch('exchange_rates.services.akchabar.AkchabarGatewayHttpClient') as MockHttpClient:
        mock_client_instance = MockHttpClient.return_value
        mock_response = mock_client_instance.get.return_value
        mock_response.json.return_value = mock_response_data

        # Мокаем контекстный менеджер
        with patch('exchange_rates.services.akchabar.create_akchabar_gateway_http_client',
                   return_value=mock_client_instance):
            # Act
            ExchangeRatesFetchAndUpdateUseCase().execute()

    # Assert - проверяем, что записи созданы в БД
    exchange_rates = list(ExchangeRate.objects.all())
    assert len(exchange_rates) == 2

    # Создаем словарь для удобства проверки
    rates_dict = {rate.currency_code: rate for rate in exchange_rates}

    # Проверяем USD
    assert 'usd' in rates_dict
    usd_rate = rates_dict['usd']
    assert usd_rate.rate == Decimal('87.50')
    assert usd_rate.updated_at == expected_datetime

    # Проверяем EUR
    assert 'eur' in rates_dict
    eur_rate = rates_dict['eur']
    assert eur_rate.rate == Decimal('99.75')
    assert eur_rate.updated_at == expected_datetime


@pytest.mark.django_db
def test_exchange_rates_fetch_and_update_updates_existing_rates():
    # Arrange - создаем существующие курсы
    old_time = datetime.datetime.now(tz=ZoneInfo("Asia/Bishkek"))

    usd_rate = ExchangeRate.objects.create(
        currency_code=ExchangeRate.CurrencyCode.USD,
        rate=Decimal('85.25'),
        updated_at=old_time,
    )

    # Подготавливаем mock-данные для ответа API с новыми курсами
    mock_response_data = {
        'date': '19.04.2025',
        'time': '19:45:00',
        'rate_values': [
            {'currency': 'usd', 'buy_rate': '87.50'},
            {'currency': 'rub', 'buy_rate': '0.97'},  # Новая валюта
        ]
    }

    expected_datetime = datetime.datetime.combine(
        date=datetime.datetime.strptime('19.04.2025', '%d.%m.%Y'),
        time=datetime.time.fromisoformat('19:45:00'),
        tzinfo=ZoneInfo("Asia/Bishkek"),
    )

    # Мокаем ответ HTTP клиента
    with patch('exchange_rates.services.akchabar.AkchabarGatewayHttpClient') as MockHttpClient:
        mock_client_instance = MockHttpClient.return_value
        mock_response = mock_client_instance.get.return_value
        mock_response.json.return_value = mock_response_data

        # Мокаем контекстный менеджер
        with patch('exchange_rates.services.akchabar.create_akchabar_gateway_http_client',
                   return_value=mock_client_instance):
            # Act
            ExchangeRatesFetchAndUpdateUseCase().execute()

    # Assert - проверяем, что записи обновлены и добавлены в БД
    exchange_rates = list(ExchangeRate.objects.all())
    assert len(exchange_rates) == 2  # Теперь у нас USD и RUB

    # Проверяем обновление USD
    usd_rate.refresh_from_db()
    assert usd_rate.rate == Decimal('87.50')
    assert usd_rate.updated_at == expected_datetime

    # Проверяем создание RUB
    assert ExchangeRate.objects.filter(currency_code=ExchangeRate.CurrencyCode.RUB).exists()
    rub_rate = ExchangeRate.objects.get(currency_code=ExchangeRate.CurrencyCode.RUB)
    assert rub_rate.rate == Decimal('0.97')
    assert rub_rate.updated_at == expected_datetime
