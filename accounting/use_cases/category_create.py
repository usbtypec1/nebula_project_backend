from dataclasses import dataclass

from accounting.services.categories import (
    CategoryCreateResultDto,
    create_category, ensure_category_exists,
)
from telegram_auth.services import ensure_user_exists


@dataclass(frozen=True, slots=True, kw_only=True)
class CategoryCreateUseCase:
    name: str
    parent_id: int | None
    user_id: int
    type: int

    def execute(self) -> CategoryCreateResultDto:
        ensure_user_exists(self.user_id)
        if self.parent_id is not None:
            ensure_category_exists(self.parent_id)
        return create_category(
            user_id=self.user_id,
            name=self.name,
            type=self.type,
            parent_id=self.parent_id,
        )
