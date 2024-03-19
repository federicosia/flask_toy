from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(description="User name")
    surname: str = Field(description="User surname")
    email: str = Field(description="User email")
    discount_points: int = Field(default=0, description="User discount points available")
