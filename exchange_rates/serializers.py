from rest_framework import serializers

from exchange_rates.models import ExchangeRate


class ExchangeRateListOutputSerializer(serializers.Serializer):
    source_name = serializers.CharField()
    logo_url = serializers.URLField(allow_null=True)
    buy_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    sell_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency_code = serializers.ChoiceField(
        choices=ExchangeRate.CurrencyCode.choices,
    )
    updated_at = serializers.DateTimeField()
