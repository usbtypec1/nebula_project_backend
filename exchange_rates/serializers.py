from rest_framework import serializers

from exchange_rates.models import ExchangeRate


class ExchangeRateListOutputSerializer(serializers.Serializer):
    rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency_code = serializers.ChoiceField(
        choices=ExchangeRate.CurrencyCode.choices,
    )
    updated_at = serializers.DateTimeField()
