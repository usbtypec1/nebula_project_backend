from django.urls import path

from exchange_rates.views import ExchangeRateListApi


urlpatterns = [
    path(
        '', ExchangeRateListApi.as_view(),
        name='exchange-rate-list',
    ),
]
