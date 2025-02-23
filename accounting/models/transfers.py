from django.db import models
from django.utils.translation import gettext_lazy as _

from accounting.models.accounts import Account


class Transfer(models.Model):
    from_account = models.ForeignKey(
        to=Account,
        on_delete=models.PROTECT,
        related_name='transfers_from',
        verbose_name=_('From account'),
    )
    to_account = models.ForeignKey(
        to=Account,
        on_delete=models.PROTECT,
        related_name='transfers_to',
        verbose_name=_('To account'),
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
        verbose_name = _('Transfer')
        verbose_name_plural = _('Transfers')
        constraints = (
            models.CheckConstraint(
                check=~models.Q(from_account=models.F('to_account')),
                name='prevent_self_transfer',
            ),
        )
        indexes = (
            models.Index(fields=('from_account',)),
            models.Index(fields=('to_account',)),
        )
