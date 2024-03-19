from typing import Optional

from pydantic import BaseModel, Field


class CategoryQuery(BaseModel):
    num_page: Optional[int] = Field(default=1, ge=1, description="Page number")
    type: str = Field(description="Category selected")


class CategoriesResponse(BaseModel):
    num_products_per_categories: dict[str, int] = Field(description="Map with number of products per categories")
