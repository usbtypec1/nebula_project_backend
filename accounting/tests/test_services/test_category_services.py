import pytest

from accounting.models import Category
from accounting.services.categories import CategoryListDto, CategoryListItemDto, get_categories_page
from accounting.tests.factories import CategoryFactory
from telegram_auth.tests.factories import UserFactory

# Проверяет, что функция get_categories_page возвращает корректные объекты DTO
#с правильными данными из базы данных.
@pytest.mark.django_db
def test_get_categories_page_returns_correct_dto():
    # Arrange
    user = UserFactory()
    category = CategoryFactory(user=user, type=Category.Type.EXPENSE)

    # Act
    result = get_categories_page(
        user_id=user.id,
        category_type=Category.Type.EXPENSE,
    )

    # Assert
    assert isinstance(result, CategoryListDto)
    assert result.user_id == user.id
    assert len(result.categories) == 1
    assert isinstance(result.categories[0], CategoryListItemDto)


# Проверяет правильность структуры и полей объекта DTO категории.
@pytest.mark.django_db
def test_category_dto_has_correct_fields():
    # Arrange
    user = UserFactory()
    category = CategoryFactory(user=user, type=Category.Type.EXPENSE)

    # Act
    result = get_categories_page(
        user_id=user.id,
        category_type=Category.Type.EXPENSE,
    )
    dto = result.categories[0]

    # Assert
    assert dto.id == category.id
    assert dto.name == category.name
    assert dto.type == category.type
    assert dto.parent_id == category.parent_id
    assert dto.created_at == category.created_at
    assert dto.updated_at == category.updated_at


# Проверяет корректность фильтрации по типу категории EXPENSE.
@pytest.mark.django_db
def test_get_categories_page_filter_expense_type():
    # Arrange
    user = UserFactory()
    expense_category = CategoryFactory(user=user, type=Category.Type.EXPENSE)
    income_category = CategoryFactory(user=user, type=Category.Type.INCOME)

    # Act - filter by expense type
    expense_result = get_categories_page(
        user_id=user.id,
        category_type=Category.Type.EXPENSE,
    )

    # Assert
    assert len(expense_result.categories) == 1
    assert expense_result.categories[0].id == expense_category.id
    assert expense_result.categories[0].type == Category.Type.EXPENSE


# Проверяет корректность фильтрации по типу категории INCOME.
@pytest.mark.django_db
def test_get_categories_page_filter_income_type():
    # Arrange
    user = UserFactory()
    expense_category = CategoryFactory(user=user, type=Category.Type.EXPENSE)
    income_category = CategoryFactory(user=user, type=Category.Type.INCOME)

    # Act - filter by income type
    income_result = get_categories_page(
        user_id=user.id,
        category_type=Category.Type.INCOME,
    )

    # Assert
    assert len(income_result.categories) == 1
    assert income_result.categories[0].id == income_category.id
    assert income_result.categories[0].type == Category.Type.INCOME


# Проверяет, что при отсутствии фильтра по типу возвращаются все категории.
@pytest.mark.django_db
def test_get_categories_page_with_no_type_filter():
    # Arrange
    user = UserFactory()
    expense_category = CategoryFactory(user=user, type=Category.Type.EXPENSE)
    income_category = CategoryFactory(user=user, type=Category.Type.INCOME)

    # Act - no type filter
    result = get_categories_page(
        user_id=user.id,
        category_type=None,
    )

    # Assert
    assert len(result.categories) == 2
    category_ids = {category.id for category in result.categories}
    assert expense_category.id in category_ids
    assert income_category.id in category_ids


# Проверяет, что функция корректно обрабатывает случай, когда у пользователя нет категорий.
@pytest.mark.django_db
def test_get_categories_page_empty_result():
    # Arrange
    user = UserFactory()
    # No categories created

    # Act
    result = get_categories_page(
        user_id=user.id,
        category_type=Category.Type.EXPENSE,
    )

    # Assert
    assert result.user_id == user.id
    assert result.categories == []


# Проверяет, что структура родитель-потомки корректно отображается в результате.
@pytest.mark.django_db
def test_get_categories_page_parent_child_structure():
    # Arrange
    user = UserFactory()

    # Create parent category
    parent = CategoryFactory(
        user=user,
        type=Category.Type.EXPENSE,
        name="Parent Category"
    )

    # Create child categories
    child1 = CategoryFactory(
        user=user,
        type=Category.Type.EXPENSE,
        parent=parent,
        name="Child Category 1"
    )

    # Act
    result = get_categories_page(
        user_id=user.id,
        category_type=Category.Type.EXPENSE,
    )

    # Assert
    assert len(result.categories) == 2

    # Find each category in the results
    parent_dto = next((c for c in result.categories if c.id == parent.id), None)
    child1_dto = next((c for c in result.categories if c.id == child1.id), None)

    assert parent_dto is not None
    assert child1_dto is not None

    # Check parent-child relationships
    assert parent_dto.parent_id is None
    assert child1_dto.parent_id == parent.id


# Проверяет, что в результате корректно отображаются несколько дочерних категорий.
@pytest.mark.django_db
def test_get_categories_page_multiple_children():
    # Arrange
    user = UserFactory()

    # Create parent category
    parent = CategoryFactory(
        user=user,
        type=Category.Type.EXPENSE,
        name="Parent Category"
    )

    # Create child categories
    child1 = CategoryFactory(
        user=user,
        type=Category.Type.EXPENSE,
        parent=parent,
        name="Child Category 1"
    )

    child2 = CategoryFactory(
        user=user,
        type=Category.Type.EXPENSE,
        parent=parent,
        name="Child Category 2"
    )

    # Act
    result = get_categories_page(
        user_id=user.id,
        category_type=Category.Type.EXPENSE,
    )

    # Assert
    assert len(result.categories) == 3

    # Find each category in the results
    child_categories = [c for c in result.categories if c.parent_id == parent.id]
    assert len(child_categories) == 2


# Проверяет корректность отображения многоуровневой иерархии категорий
#(родитель-потомок-потомок потомка).
@pytest.mark.django_db
def test_get_categories_page_with_multi_level_hierarchy():
    # Arrange
    user = UserFactory()

    # Create a three-level hierarchy
    grandparent = CategoryFactory(
        user=user,
        type=Category.Type.EXPENSE,
        name="Grandparent"
    )

    parent = CategoryFactory(
        user=user,
        type=Category.Type.EXPENSE,
        parent=grandparent,
        name="Parent"
    )

    child = CategoryFactory(
        user=user,
        type=Category.Type.EXPENSE,
        parent=parent,
        name="Child"
    )

    # Act
    result = get_categories_page(
        user_id=user.id,
        category_type=Category.Type.EXPENSE,
    )

    # Assert
    assert len(result.categories) == 3

    # Extract each category
    grandparent_dto = next((c for c in result.categories if c.id == grandparent.id), None)
    parent_dto = next((c for c in result.categories if c.id == parent.id), None)
    child_dto = next((c for c in result.categories if c.id == child.id), None)

    assert grandparent_dto is not None
    assert parent_dto is not None
    assert child_dto is not None

    # Check hierarchy relationships
    assert grandparent_dto.parent_id is None
    assert parent_dto.parent_id == grandparent.id
    assert child_dto.parent_id == parent.id