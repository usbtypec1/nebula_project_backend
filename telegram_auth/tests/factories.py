import factory
from factory.django import DjangoModelFactory

from telegram_auth.models import User


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    telegram_id = factory.Faker("random_int", min=10000000, max=999999999)
    full_name = factory.Faker("name")
    username = None
    is_admin = False
    is_active = True
