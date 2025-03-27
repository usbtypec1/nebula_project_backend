import pytest
from django.urls import reverse
from rest_framework import status

from accounting.tests.factories import AccountFactory


@pytest.mark.django_db
def test_account_created_successfully(authorized_client):
    data = {
        'name': 'Card',
        'is_public': False,
    }
    url = reverse('accounting:account-list-create')

    response = authorized_client.post(url, data=data, format='json')

    response_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert response_data == {
        'id': response_data['id'],
        'name': 'Card',
        'is_public': False,
        'initial_balance': '0.00',
        'created_at': response_data['created_at'],
    }


@pytest.mark.django_db
def test_account_already_exists(user, authorized_client):
    account = AccountFactory(user=user)
    data = {
        'name': account.name,
        'is_public': False,
    }
    url = reverse('accounting:account-list-create')

    response = authorized_client.post(url, data=data, format='json')

    response_data = response.json()
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response_data == {
        'type': 'client_error',
        'errors': [
            {
                'code': 'account_already_exists',
                'detail': 'Account already exists',
            },
        ],
    }


@pytest.mark.django_db
def test_create_account_with_initial_balance(authorized_client):
    data = {
        'name': 'Card',
        'is_public': False,
        'initial_balance': '500.55'
    }
    url = reverse('accounting:account-list-create')

    response = authorized_client.post(url, data=data, format='json')

    response_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert response_data == {
        'id': response_data['id'],
        'name': 'Card',
        'is_public': False,
        'initial_balance': '500.55',
        'created_at': response_data['created_at'],
    }
