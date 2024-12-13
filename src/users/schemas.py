from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(
        examples=["Jane Smith"],
        min_length=2,
        max_length=30,
        description="The user's full name. Must be between 2 and 30 characters.",
    )
    phone: str | None = Field(
        examples=["380331234567"],
        default=None,
        description="The user's phone number. Must be a valid phone number format.",
    )
    email: EmailStr = Field(
        examples=["jane_smith@hot.com"],
        description="The user's email address. Must be a valid email format.",
    )

class UserCreate(UserBase):
    password: str = Field(
        examples=["Ramazoti_12345"],
        min_length=8,
        description="The user's password. Must be at least 8 characters long and include at least one digit, one lowercase letter, one uppercase letter, and one special character.",
    )

class UserResponse(UserBase):
    user_id: uuid.UUID = Field(examples=[str(uuid.uuid4())])

    created_at: datetime = Field(examples=["2022-02-24T07:59:03.913Z"])
    updated_at: datetime = Field(examples=["2022-02-24T07:59:03.913Z"])


class PrivateUser(UserResponse):
    model_config = ConfigDict(from_attributes=True)
    password: str


class TokenModel(BaseModel):
    access_token: str
    token_type: str = "bearer"