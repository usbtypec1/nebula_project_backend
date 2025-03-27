import pytest

from accounting.exceptions import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
)
from accounting.models import Category
from accounting.services.categories import CategoryCreateResultDto
from accounting.tests.factories import CategoryFactory
from accounting.use_cases import CategoryCreateUseCase
from telegram_auth.exceptions import UserNotFoundError
from telegram_auth.tests.factories import UserFactory


@pytest.mark.django_db
def test_category_successfully_created():
    user = UserFactory()

    result = CategoryCreateUseCase(
        name='Food',
        parent_id=None,
        user_id=user.id,
        type=Category.Type.EXPENSE,
    ).execute()

    assert result == CategoryCreateResultDto(
        id=result.id,
        name='Food',
        parent_id=None,
        user_id=user.id,
        type=Category.Type.EXPENSE,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )


@pytest.mark.django_db
def test_parent_category_not_found():
    user = UserFactory()

    with pytest.raises(CategoryNotFoundError):
        CategoryCreateUseCase(
            name='Food',
            parent_id=1,
            user_id=user.id,
            type=Category.Type.EXPENSE,
        ).execute()


@pytest.mark.django_db
def test_user_not_found():
    with pytest.raises(UserNotFoundError):
        CategoryCreateUseCase(
            name='Food',
            parent_id=None,
            user_id=12345,
            type=Category.Type.EXPENSE,
        ).execute()


@pytest.mark.django_db
def test_subcategory_successfully_created():
    parent = CategoryFactory()

    result = CategoryCreateUseCase(
        name='Food',
        parent_id=parent.id,
        user_id=parent.user.id,
        type=Category.Type.EXPENSE,
    ).execute()

    assert result == CategoryCreateResultDto(
        id=result.id,
        name='Food',
        parent_id=parent.id,
        user_id=parent.user.id,
        type=Category.Type.EXPENSE,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )


@pytest.mark.django_db
def test_category_with_this_name_already_exists():
    category = CategoryFactory()

    with pytest.raises(CategoryAlreadyExistsError):
        CategoryCreateUseCase(
            name=category.name,
            parent_id=None,
            user_id=category.user.id,
            type=category.type,
        ).execute()
