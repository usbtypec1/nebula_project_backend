from django.db import models
from django.utils.translation import gettext_lazy as _

from accounting.models.accounts import Account
from accounting.models.categories import Category


class Transaction(models.Model):
    account = models.ForeignKey(
        to=Account,
        on_delete=models.PROTECT,
        verbose_name=_('Account'),
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        verbose_name=_('Category'),
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Amount'),
    )
    description = models.TextField(
        max_length=1024,
        blank=True,
        null=True,
        verbose_name=_('Description'),
    )
    date = models.DateTimeField(
        verbose_name=_('Date'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        indexes = (
            models.Index(fields=('account',)),
            models.Index(fields=('category',)),
        )
