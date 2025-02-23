from django.db import models
from django.utils.translation import gettext_lazy as _

from accounting.models.accounts import Account
from telegram_auth.models import User


class SharedAccount(models.Model):
    account = models.ForeignKey(
        to=Account,
        on_delete=models.CASCADE,
        verbose_name=_('Account'),
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    class Meta:
        verbose_name = _('Shared account')
        verbose_name_plural = _('Shared accounts')
        constraints = (
            models.UniqueConstraint(
                fields=('account', 'user'),
                name='unique_shared_account_per_user',
            ),
        )
