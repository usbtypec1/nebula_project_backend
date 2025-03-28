from dataclasses import dataclass

from accounting.services.categories import (
    delete_category_by_id,
    ensure_category_permission_allowed,
    get_category_by_id,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class CategoryDeleteUseCase:
    category_id: int
    user_id: int

    def execute(self) -> None:
        category = get_category_by_id(category_id=self.category_id)
        ensure_category_permission_allowed(
            category=category,
            user_id=self.user_id,
        )
        delete_category_by_id(self.category_id)
