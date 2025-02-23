from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class CategoryCreateResult:
    pass


@dataclass(frozen=True, slots=True, kw_only=True)
class CategoryCreateUseCase:
    name: str
    parent_id: int | None
    user_id: int
    type: int

    def execute(self) -> CategoryCreateResult:
        pass
