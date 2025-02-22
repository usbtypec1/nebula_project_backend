from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from telegram_auth.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    ordering = ['telegram_id']

    list_display = ('telegram_id', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active')

    fieldsets = (
        (_('Login Info'), {'fields': ('telegram_id', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin')}),
    )

    add_fieldsets = (
        (_('Create New User'), {
            'classes': ('wide',),
            'fields': (
            'telegram_id', 'password1', 'password2', 'is_active', 'is_admin'),
        }),
    )

    search_fields = ('telegram_id',)
    filter_horizontal = ()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_admin=False)
