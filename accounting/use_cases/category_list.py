from dataclasses import dataclass

from accounting.services.categories import CategoryListDto, get_categories_page


@dataclass(frozen=True, slots=True, kw_only=True)
class CategoryListUseCase:
    user_id: int
    category_type: int | None

    def execute(self) -> CategoryListDto:
        return get_categories_page(
            user_id=self.user_id,
            category_type=self.category_type,
        )
