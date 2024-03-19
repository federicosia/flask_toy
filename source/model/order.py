import uuid
from enum import Enum

from pydantic import BaseModel, Field


class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Id to identify univocally orders")
    user_email: str = Field(description="User email")
    products: list = Field(description="Products choosed by the customer")
    total: float = Field(description="Total cost of the order")
    discount_applied: int = Field(default=0, description="Discount applied in euros")
    discount_points_earned: int = Field(default=0, description="Discount points earned making this order")
    payment_info: dict = Field(default={}, description="Payment informations")


class OrderBody(BaseModel):
    products: list = Field(description="Products choosed by the customer")
    email: str = Field(description="User email")
    total: float = Field(description="Total cost of the order")
    payment_info: dict = Field(default={}, description="Payment informations")


class OrderResult(str, Enum):
    success: str = "The order was successfully made"
    rejected: str = "The order couldn't be made for credit insufficient"


class OrderResponse(BaseModel):
    outcome: str = Field(description="Outcome of the order")
    total: float = Field(description="Total cost of the order")
    discount_points_earned: int = Field(default=0, description="Discount points earned making this order")
