from django.contrib import admin

from exchange_rates.models import ExchangeRate


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = (
        'source_name',
        'buy_rate',
        'sell_rate',
        'currency_code',
        'updated_at',
    )
    list_filter = ('currency_code',)
    search_fields = ('source_name',)
