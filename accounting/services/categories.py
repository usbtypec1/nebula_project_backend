import datetime
from collections.abc import Iterable
from dataclasses import dataclass

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
        categories=map_categories_to_dto(categories),
        is_end_of_list_reached=is_end_of_list_reached,
    )
