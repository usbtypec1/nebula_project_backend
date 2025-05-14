import pytest

from accounting.models import Category
from accounting.services.categories import CategoryListDto, CategoryListItemDto
from accounting.tests.factories import CategoryFactory
from accounting.use_cases import CategoryListUseCase
from telegram_auth.tests.factories import UserFactory


# Проверяет, что одна категория корректно возвращается в списке
@pytest.mark.django_db
def test_single_category():
    user = UserFactory()
    category = CategoryFactory(type=Category.Type.EXPENSE, user=user)

    result = CategoryListUseCase(
        user_id=user.id,
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
    )


# Проверяет, что если у пользователя нет категорий, возвращается пустой список
@pytest.mark.django_db
def test_no_categories():
    user = UserFactory()

    result = CategoryListUseCase(
        user_id=user.id,
        category_type=Category.Type.EXPENSE,
    ).execute()

    assert result == CategoryListDto(
        user_id=user.id,
        categories=[],
    )


# Проверяет, что возвращаются только категории типа "расход"
@pytest.mark.django_db
def test_filter_expense_categories_only():
    user = UserFactory()
    expense_category = CategoryFactory(type=Category.Type.EXPENSE, user=user)
    CategoryFactory(type=Category.Type.INCOME, user=user)

    result = CategoryListUseCase(
        user_id=user.id,
        category_type=Category.Type.EXPENSE,
    ).execute()

    assert len(result.categories) == 1
    assert result.categories[0].type == Category.Type.EXPENSE
    assert result.categories[0].name == expense_category.name


# Проверяет, что возвращаются только категории типа "доход"
@pytest.mark.django_db
def test_filter_income_categories_only():
    user = UserFactory()
    CategoryFactory(type=Category.Type.EXPENSE, user=user)
    income_category = CategoryFactory(type=Category.Type.INCOME, user=user)

    result = CategoryListUseCase(
        user_id=user.id,
        category_type=Category.Type.INCOME,
    ).execute()

    assert len(result.categories) == 1
    assert result.categories[0].type == Category.Type.INCOME
    assert result.categories[0].name == income_category.name


# Проверяет, что при отсутствии фильтра по типу возвращаются все категории пользователя
@pytest.mark.django_db
def test_all_categories_no_filter():
    user = UserFactory()
    CategoryFactory(type=Category.Type.EXPENSE, user=user)
    CategoryFactory(type=Category.Type.INCOME, user=user)

    result = CategoryListUseCase(
        user_id=user.id,
        category_type=None,
    ).execute()

    assert len(result.categories) == 2
    assert {cat.type for cat in result.categories} == {Category.Type.EXPENSE, Category.Type.INCOME}


# Проверяет, что возвращаются все категории одного типа
# И имена совпадают с созданными
@pytest.mark.django_db
def test_multiple_expense_categories():
    user = UserFactory()
    categories = CategoryFactory.create_batch(3, type=Category.Type.EXPENSE, user=user)

    result = CategoryListUseCase(
        user_id=user.id,
        category_type=Category.Type.EXPENSE,
    ).execute()

    assert len(result.categories) == 3
    result_names = {category.name for category in result.categories}
    expected_names = {category.name for category in categories}
    assert result_names == expected_names


# Проверяет отношения родитель-дочерняя категория
@pytest.mark.django_db
def test_parent_and_child_categories():
    user = UserFactory()
    parent_category = CategoryFactory(type=Category.Type.EXPENSE, user=user, name="Родительская категория")
    child_category = CategoryFactory(type=Category.Type.EXPENSE, user=user, parent=parent_category, name="Дочерняя категория")

    result = CategoryListUseCase(
        user_id=user.id,
        category_type=Category.Type.EXPENSE,
    ).execute()

    assert len(result.categories) == 2
    parent_dto = next((c for c in result.categories if c.parent_id is None), None)
    child_dto = next((c for c in result.categories if c.parent_id is not None), None)

    assert parent_dto.name == parent_category.name
    assert child_dto.name == child_category.name
    assert child_dto.parent_id == parent_category.id


# Проверяет, что категории первого пользователя не попадают в результат второго
@pytest.mark.django_db
def test_categories_are_user_specific_user1():
    user1 = UserFactory()
    user2 = UserFactory()
    category_user1 = CategoryFactory(type=Category.Type.EXPENSE, user=user1, name="Категория пользователя 1")
    CategoryFactory(type=Category.Type.EXPENSE, user=user2, name="Категория пользователя 2")

    result_user1 = CategoryListUseCase(
        user_id=user1.id,
        category_type=Category.Type.EXPENSE,
    ).execute()

    assert len(result_user1.categories) == 1
    assert result_user1.categories[0].name == category_user1.name


# Проверяет, что категории второго пользователя не попадают в результат первого
@pytest.mark.django_db
def test_categories_are_user_specific_user2():
    user1 = UserFactory()
    user2 = UserFactory()
    CategoryFactory(type=Category.Type.EXPENSE, user=user1, name="Категория пользователя 1")
    category_user2 = CategoryFactory(type=Category.Type.EXPENSE, user=user2, name="Категория пользователя 2")

    result_user2 = CategoryListUseCase(
        user_id=user2.id,
        category_type=Category.Type.EXPENSE,
    ).execute()

    assert len(result_user2.categories) == 1
    assert result_user2.categories[0].name == category_user2.name