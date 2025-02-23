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
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name=_('User'),
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
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name
