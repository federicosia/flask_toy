from pydantic import BaseModel, Field


class PageNotFoundError(BaseModel):
    error_code: int = Field(default=404)
    description: str = Field(default="The page requested was not found...")


class BadRequestError(BaseModel):
    error_code: int = Field(default=400)
    description: str = Field(default="Bad request")


class BadRequestMalformedBodyOrderError(BadRequestError):
    description: str = Field(default="The request received has missing informations in the body or bad formatting")


class PaymentRequiredError(BaseModel):
    error_code: int = Field(default=402)
    description: str = Field(default="Credit card does not have sufficient funds to make the order")
