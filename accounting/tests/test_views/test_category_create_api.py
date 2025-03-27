import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounting.models import Category
from accounting.tests.factories import CategoryFactory


@pytest.mark.django_db
def test_create_category_without_parent(authorized_client):
    url = reverse('accounting:category-list-create')
    data = {
        'name': 'Food',
        'type': Category.Type.EXPENSE,
    }

    response = authorized_client.post(url, format='json', data=data)

    response_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert response_data == {
        'id': response_data['id'],
        'name': 'Food',
        'type': Category.Type.EXPENSE,
        'parent_id': None,
        'created_at': response_data['created_at'],
        'updated_at': response_data['updated_at'],
    }


@pytest.mark.django_db
def test_user_not_authenticated():
    client = APIClient()
    url = reverse('accounting:category-list-create')
    data = {
        'name': 'Food',
        'type': Category.Type.EXPENSE,
    }

    response = client.post(url, format='json', data=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        'type': 'client_error',
        'errors': [
            {
                'code': 'not_authenticated',
                'detail': 'Authentication credentials were not provided.',
            },
        ],
    }


@pytest.mark.django_db
def test_create_subcategory(authorized_client):
    category = CategoryFactory()
    url = reverse('accounting:category-list-create')
    data = {
        'name': 'Food',
        'parent_id': category.id,
        'type': Category.Type.EXPENSE,
    }

    response = authorized_client.post(url, format='json', data=data)

    response_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert response_data == {
        'id': response_data['id'],
        'name': 'Food',
        'type': Category.Type.EXPENSE,
        'parent_id': category.id,
        'created_at': response_data['created_at'],
        'updated_at': response_data['updated_at'],
    }


@pytest.mark.django_db
def test_category_already_exists(user, authorized_client):
    category = CategoryFactory(user=user)
    url = reverse('accounting:category-list-create')
    data = {
        'name': category.name,
        'parent_id': None,
        'type': category.type,
    }

    response = authorized_client.post(url, format='json', data=data)

    response_data = response.json()
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response_data == {
        'type': 'client_error',
        'errors': [
            {
                'code': 'category_already_exists',
                'detail': 'Category already exists'
            }
        ]
    }
