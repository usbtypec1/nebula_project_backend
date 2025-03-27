import pytest

from accounting.models import Category
from accounting.services.categories import CategoryListDto, CategoryListItemDto
from accounting.tests.factories import CategoryFactory
from accounting.use_cases import CategoryListUseCase
from telegram_auth.exceptions import UserNotFoundError
from telegram_auth.tests.factories import UserFactory


@pytest.mark.django_db
def test_single_category():
    user = UserFactory()
    category = CategoryFactory(type=Category.Type.EXPENSE, user=user)

    result = CategoryListUseCase(
        user_id=user.id,
        take=1000,
        skip=0,
        category_type=Category.Type.EXPENSE,
    ).execute()

    assert result == CategoryListDto(
        user_id=user.id,
        categories=[
            CategoryListItemDto(
                id=result.categories[0].id,
                name=category.name,
                parent_id=None,
                type=Category.Type.EXPENSE,
                created_at=result.categories[0].created_at,
                updated_at=result.categories[0].updated_at,
            ),
        ],
        is_end_of_list_reached=True,
    )


@pytest.mark.django_db
def test_no_categories():
    user = UserFactory()

    result = CategoryListUseCase(
        user_id=user.id,
        take=1000,
        skip=0,
        category_type=Category.Type.EXPENSE,
    ).execute()

    assert result == CategoryListDto(
        user_id=user.id,
        categories=[],
        is_end_of_list_reached=True,
    )


@pytest.mark.django_db
def test_user_not_found():
    with pytest.raises(UserNotFoundError):
        CategoryListUseCase(
            user_id=12345,
            take=1000,
            skip=0,
            category_type=None,
        ).execute()


@pytest.mark.django_db
def test_category_has_next_page():
    user = UserFactory()
    CategoryFactory.create_batch(2, user=user)

    result = CategoryListUseCase(
        user_id=user.id,
        take=1,
        skip=0,
        category_type=None,
    ).execute()

    assert result.is_end_of_list_reached is False
