from dataclasses import dataclass

from accounting.services.categories import CategoryListDto, get_categories_page


@dataclass(frozen=True, slots=True, kw_only=True)
class CategoryListUseCase:
    user_id: int
    take: int
    skip: int
    category_type: int

    def execute(self) -> CategoryListDto:
        return get_categories_page(
            user_id=self.user_id,
            take=self.take,
            skip=self.skip,
            category_type=self.category_type,
        )
