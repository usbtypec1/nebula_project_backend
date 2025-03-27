from django.db import models
from django.utils.translation import gettext_lazy as _

from telegram_auth.models import User


class Account(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name=_('Account name'),
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        verbose_name=_('User'),
    )
    initial_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('Initial balance'),
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name=_('Is public'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'user'),
                name='unique_account_per_user',
            ),
        )
        indexes = (
            models.Index(fields=('user',)),
        )

    def __str__(self):
        return self.name
