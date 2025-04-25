from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status

from exchange_rates.models import ExchangeRate
from exchange_rates.tests.factories import ExchangeRateFactory


@pytest.mark.django_db
def test_exchange_rate_list_success(client):
    url = reverse('exchange-rate-list')
    ExchangeRateFactory.create_batch(3)

    response = client.get(url, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'exchange_rates' in response.data
    assert len(response.data['exchange_rates']) == 3


@pytest.mark.django_db
def test_exchange_rate_list_empty(client):
    url = reverse('exchange-rate-list')

    response = client.get(url, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'exchange_rates' in response.data
    assert len(response.data['exchange_rates']) == 0


@pytest.mark.django_db
def test_exchange_rate_list_response_structure(client):
    url = reverse('exchange-rate-list')
    rate = ExchangeRateFactory(
        currency_code=ExchangeRate.CurrencyCode.USD,
        rate=Decimal('83.50')
    )

    response = client.get(url, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'exchange_rates' in response.data

    exchange_rate = response.data['exchange_rates'][0]
    assert 'currency_code' in exchange_rate
    assert 'rate' in exchange_rate
    assert 'updated_at' in exchange_rate

    assert exchange_rate['currency_code'] == 'usd'
    assert Decimal(exchange_rate['rate']) == Decimal('83.50')


@pytest.mark.django_db
def test_exchange_rate_list_without_auth(client):
    url = reverse('exchange-rate-list')

    response = client.get(url, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'exchange_rates' in response.data
    assert len(response.data['exchange_rates']) == 0
    assert response.data['exchange_rates'] == []