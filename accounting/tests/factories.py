import factory
from django.utils.timezone import now

from accounting.models import Category
from telegram_auth.tests.factories import UserFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    user = factory.SubFactory(UserFactory)
    name = factory.Faker("word")
    type = factory.Iterator([Category.Type.INCOME, Category.Type.EXPENSE])
    parent = None
    updated_at = factory.LazyFunction(now)
    created_at = factory.LazyFunction(now)
