from django.urls import path
from exchange_rates.views import get_rates

urlpatterns = [
    path('', get_rates, name="get-rates")
]