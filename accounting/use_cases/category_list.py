from dataclasses import dataclass

from accounting.services.categories import CategoryListDto, get_categories_page
from telegram_auth.services import ensure_user_exists


@dataclass(frozen=True, slots=True, kw_only=True)
class CategoryListUseCase:
    user_id: int
    take: int
    skip: int
    category_type: int | None

    def execute(self) -> CategoryListDto:
        ensure_user_exists(self.user_id)
        return get_categories_page(
            user_id=self.user_id,
            take=self.take,
            skip=self.skip,
            category_type=self.category_type,
        )
