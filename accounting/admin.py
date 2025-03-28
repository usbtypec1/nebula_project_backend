from django.contrib import admin

from accounting.models import (
    Account, SharedAccount, Category, Transfer,
    Transaction,
)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(SharedAccount)
class SharedAccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass