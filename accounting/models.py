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


class Category(models.Model):
    class Type(models.IntegerChoices):
        INCOME = 1, _('Income')
        EXPENSE = 2, _('Expense')

    user = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        verbose_name=_('User'),
    )
    name = models.CharField(
        max_length=64,
        verbose_name=_('Category name'),
    )
    type = models.PositiveSmallIntegerField(
        choices=Type.choices,
        verbose_name=_('Type'),
    )
    parent = models.ForeignKey(
        to='self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_('Parent category'),
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
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        indexes = (
            models.Index(fields=('user', 'type')),
        )
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'user', 'type'),
                name='unique_category_per_user',
            ),
        )


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
