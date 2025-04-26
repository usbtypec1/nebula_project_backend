from django.contrib import admin

from accounting.models import (
    Account, SharedAccount, Category, Transfer,
    Transaction,
)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    list_select_related = ('user',)
    list_filter = ('is_public',)


@admin.register(SharedAccount)
class SharedAccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'type')
    list_select_related = ('user',)
    list_filter = ('type',)


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('from_account', 'to_account')
    list_select_related = ('from_account', 'to_account')
    date_hierarchy = 'date'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'category')
    list_select_related = ('account', 'category')
    date_hierarchy = 'date'
