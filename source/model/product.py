from typing import Optional

from pydantic import BaseModel, Field


class Product(BaseModel):
    id: str = Field(description="Id used to identify univocally a product")
    category: str = Field(description="Category of the product")
    name: str = Field(description="Name of the product")
    price: float = Field(description="Price of a single product")
    quantity: int = Field(description="Quantity of the product stored")
    image: str = Field(description="Image of the product")
    discount_multiplier: Optional[int] = Field(default=1, description="Multiplies the discount points "
                                                                      "obtained by the number of the multiplier")


class ProductQuery(BaseModel):
    page: Optional[int] = Field(default=1, description="Page number")


class SearchQuery(BaseModel):
    page: Optional[int] = Field(default=1, description="Page number")
    article: Optional[str] = Field(default="", description="Article with this substring present in the name")


class ProductResponse(BaseModel):
    products: list[Product]
