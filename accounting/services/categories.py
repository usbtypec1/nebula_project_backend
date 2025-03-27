import datetime
from collections.abc import Iterable
from dataclasses import dataclass

from django.core.exceptions import ValidationError

from accounting.exceptions import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
)
from accounting.models.categories import Category


@dataclass(frozen=True, slots=True, kw_only=True)
class CategoryListItemDto:
    id: int
    name: str
    parent_id: int | None
    type: int
    updated_at: datetime.datetime
    created_at: datetime.datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class CategoryListDto:
    user_id: int
    categories: list[CategoryListItemDto]
    is_end_of_list_reached: bool


def map_categories_to_dto(
        categories: Iterable[Category],
) -> list[CategoryListItemDto]:
    return [
        CategoryListItemDto(
            id=category.id,
            name=category.name,
            parent_id=category.parent_id,
            type=category.type,
            updated_at=category.updated_at,
            created_at=category.created_at,
        )
        for category in categories
    ]


def get_categories_page(
        *,
        user_id: int,
        take: int,
        skip: int,
        category_type: int | None = None,
) -> CategoryListDto:
    categories = Category.objects.filter(user_id=user_id)
    if category_type is not None:
        categories = categories.filter(type=category_type)

    categories = categories[skip:skip + take + 1]
    is_end_of_list_reached = len(categories) <= take
    categories = categories[:take]

    return CategoryListDto(
        user_id=user_id,
        categories=map_categories_to_dto(categories),
        is_end_of_list_reached=is_end_of_list_reached,
    )


def ensure_category_exists(category_id: int) -> None:
    if not Category.objects.filter(id=category_id).exists():
        raise CategoryNotFoundError


@dataclass(frozen=True, slots=True, kw_only=True)
class CategoryCreateResultDto:
    id: int
    name: str
    parent_id: int | None
    type: int
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


def create_category(
        *,
        user_id: int,
        name: str,
        type: int,
        parent_id: int | None,
) -> CategoryCreateResultDto:
    category = Category(
        user_id=user_id,
        name=name,
        type=type,
        parent_id=parent_id,
    )
    try:
        category.full_clean()
    except ValidationError as error:
        if ('Category with this Category name, User and Type already exists.'
                in error.messages):
            raise CategoryAlreadyExistsError
        raise error

    category.save()

    return CategoryCreateResultDto(
        id=category.id,
        name=category.name,
        parent_id=category.parent_id,
        type=category.type,
        user_id=category.user_id,
        created_at=category.created_at,
        updated_at=category.updated_at,
    )
