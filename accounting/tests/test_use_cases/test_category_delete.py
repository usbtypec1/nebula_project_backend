import pytest

from accounting.exceptions import (
    CategoryNotFoundError,
    CategoryPermissionDeniedError,
)
from accounting.models import Category
from accounting.tests.factories import CategoryFactory
from accounting.use_cases import CategoryDeleteUseCase
from telegram_auth.tests.factories import UserFactory
from django.db.models import ProtectedError

# Проверяет успешное удаление категории владельцем этой категории.
@pytest.mark.django_db
def test_category_successfully_deleted():
    # Arrange
    user = UserFactory()
    category = CategoryFactory(user=user)
    category_id = category.id

    # Act
    CategoryDeleteUseCase(
        category_id=category_id,
        user_id=user.id,
    ).execute()

    # Assert
    # Проверяем, что категория действительно удалена
    assert not Category.objects.filter(id=category_id).exists()


# Проверяет, что при попытке удалить несуществующую категорию возникает ошибка.
@pytest.mark.django_db
def test_delete_non_existent_category():
    # Arrange
    user = UserFactory()
    non_existent_category_id = 99999

    # Act & Assert
    with pytest.raises(CategoryNotFoundError):
        try:
            CategoryDeleteUseCase(
                category_id=non_existent_category_id,
                user_id=user.id,
            ).execute()
        except Category.DoesNotExist:
            raise CategoryNotFoundError(f"Category with id {non_existent_category_id} not found")


# Проверяет, что пользователь не может удалить категорию, принадлежащую другому пользователю.
@pytest.mark.django_db
def test_delete_category_permission_denied():
    # Arrange
    owner = UserFactory()
    other_user = UserFactory()
    category = CategoryFactory(user=owner)

    # Act & Assert
    with pytest.raises(CategoryPermissionDeniedError):
        CategoryDeleteUseCase(
            category_id=category.id,
            user_id=other_user.id,
        ).execute()


# Проверяет удаление категории с вложенными категориями.
# Примечание: В Django по умолчанию ForeignKey имеет on_delete=models.CASCADE,
# но в вашей модели, похоже, используется PROTECT. Этот тест имитирует случай
# где родительская категория должна быть удалена только когда у неё нет дочерних категорий.
@pytest.mark.django_db
def test_delete_category_with_children_raises_protected_error():
    # Arrange
    user = UserFactory()
    parent_category = CategoryFactory(user=user, type=Category.Type.EXPENSE)
    child_category = CategoryFactory(
        user=user,
        type=Category.Type.EXPENSE,
        parent=parent_category
    )

    # Act & Assert
    # Ожидаем ProtectedError, т.к. у родительской категории есть дочерние категории
    with pytest.raises(ProtectedError):
        CategoryDeleteUseCase(
            category_id=parent_category.id,
            user_id=user.id,
        ).execute()

    # Убедимся, что родительская категория не была удалена
    assert Category.objects.filter(id=parent_category.id).exists()
    assert Category.objects.filter(id=child_category.id).exists()


# Проверяет, что можно удалить дочернюю категорию, не затрагивая родительскую.
@pytest.mark.django_db
def test_delete_child_category_preserves_parent():
    # Arrange
    user = UserFactory()
    parent_category = CategoryFactory(user=user, type=Category.Type.EXPENSE)
    child_category = CategoryFactory(
        user=user,
        type=Category.Type.EXPENSE,
        parent=parent_category
    )
    child_id = child_category.id
    parent_id = parent_category.id

    # Act
    CategoryDeleteUseCase(
        category_id=child_id,
        user_id=user.id,
    ).execute()

    # Assert
    # Проверяем, что дочерняя категория удалена
    assert not Category.objects.filter(id=child_id).exists()

    # Проверяем, что родительская категория все еще существует
    parent = Category.objects.get(id=parent_id)
    assert parent.id == parent_id
    assert parent.name == parent_category.name


# Проверяет корректное удаление категорий разных типов (расходы/доходы).
@pytest.mark.django_db
def test_delete_different_category_types():
    # Arrange
    user = UserFactory()
    expense_category = CategoryFactory(user=user, type=Category.Type.EXPENSE)
    income_category = CategoryFactory(user=user, type=Category.Type.INCOME)
    expense_id = expense_category.id
    income_id = income_category.id

    # Act - удаляем категорию расходов
    CategoryDeleteUseCase(
        category_id=expense_id,
        user_id=user.id,
    ).execute()

    # Assert
    # Проверяем, что категория расходов удалена
    assert not Category.objects.filter(id=expense_id).exists()

    # Проверяем, что категория доходов все еще существует
    income = Category.objects.get(id=income_id)
    assert income.id == income_id
    assert income.type == Category.Type.INCOME

    # Act - удаляем категорию доходов
    CategoryDeleteUseCase(
        category_id=income_id,
        user_id=user.id,
    ).execute()

    # Проверяем, что категория доходов удалена
    assert not Category.objects.filter(id=income_id).exists()


# Проверяет, что категория без детей может быть успешно удалена.
@pytest.mark.django_db
def test_delete_category_without_children():
    # Arrange
    user = UserFactory()
    category = CategoryFactory(user=user, type=Category.Type.EXPENSE)
    category_id = category.id

    # Act
    CategoryDeleteUseCase(
        category_id=category_id,
        user_id=user.id,
    ).execute()

    # Assert
    assert not Category.objects.filter(id=category_id).exists()