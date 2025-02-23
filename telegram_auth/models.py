from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):

    def create_user(
            self,
            telegram_id: int,
            full_name: str,
            password: str | None = None,
    ):
        if not telegram_id:
            raise ValueError("The User must have a telegram_id")

        user = self.model(telegram_id=telegram_id, full_name=full_name)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self, telegram_id: int, full_name: str, password: str
    ):
        user = self.create_user(telegram_id, full_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "telegram_id"  # Authenticate via telegram_id
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.telegram_id})"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
