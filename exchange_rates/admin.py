from django.contrib import admin
from exchange_rates.models import BaseExchangeRateData

@admin.register(BaseExchangeRateData)
class BaseExchangeRateDataAdmin(admin.ModelAdmin):
    list_display = ("bank_name", "currency_code", "buy_rate", "sell_rate", "updated_at")
    search_fields = ("bank_name", "currency_code")
    list_filter = ("currency_code", "bank_name")
    ordering = ("-updated_at",)