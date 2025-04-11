from django.db import models


class ExchangeRate(models.Model):
    class CurrencyCode(models.TextChoices):
        USD = 'usd', 'USD'
        EUR = 'eur', 'EUR'
        RUB = 'rub', 'RUB'
        KZT = 'kzt', 'KZT'

    currency_code = models.CharField(
        max_length=3,
        choices=CurrencyCode.choices,
    )
    buy_rate = models.DecimalField(max_digits=10, decimal_places=2)
    sell_rate = models.DecimalField(max_digits=10, decimal_places=2)
    source_name = models.CharField(max_length=255)
    logo_url = models.URLField(null=True, blank=True)
    updated_at = models.DateTimeField()

    class Meta:
        verbose_name = 'Exchange Rate'
        verbose_name_plural = 'Exchange Rates'
        constraints = (
            models.UniqueConstraint(
                fields=('source_name', 'currency_code'),
                name='unique_exchange_rate',
            ),
        )
