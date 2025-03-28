from django.db import models
from dataclasses import dataclass
from datetime import datetime

# Create your models here.

@dataclass
class ExchangeRateData:
    bank_name: str
    currency_code: str
    buy_rate: float
    sell_rate: float
    updated_at: datetime = datetime.now()


class BaseExchangeRateData(models.Model):
    bank_name = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=10)
    buy_rate = models.FloatField()
    sell_rate = models.FloatField()
    updated_at = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "Exchange Rate"
        verbose_name_plural = "Exchange Rates"

    def __str__(self):
        return f"{self.bank_name} - {self.currency_code}: {self.buy_rate}/{self.sell_rate}"