from django.db import models

from telegram_auth.models import User


class UserNotificationSettings(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='notification_settings',
    )
    transactions_gap = models.BooleanField(default=True)

    def __str__(self):
        return f"User {self.user} notification Settings"
