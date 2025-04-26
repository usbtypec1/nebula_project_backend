from django.db import models
from django.utils.translation import gettext_lazy as _

from telegram_auth.models import User


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

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'
