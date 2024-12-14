from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.adapters.orm import Role

class UserBase(BaseModel):
    username: str = Field(
        examples=["Jane Smith"],
        min_length=2,
        max_length=50,
        description="The user's full name. Must be between 2 and 30 characters.",
    )
    phone: str | None = Field(
        examples=["380331234567"],
        default=None,
        min_length=2,
        max_length=50,
        description="The user's phone number. Must be a valid phone number format.",
    )
    email: EmailStr = Field(
        examples=["jane_smith@hot.com"],
        min_length=2,
        max_length=255,
        description="The user's email address. Must be a valid email format.",
    )
    role: Role = Field(
        examples=["user"],
        default=Role.user,
        description="The role assigned to the user, defining their permissions and access level within the system.",
    )


class UserCreate(UserBase):
    password: str = Field(
        examples=["Ramazoti_12345"],
        min_length=8,
        max_length=255,
        description="The user's password. Must be at least 8 characters long.",
    )

class UserResponse(UserBase):
    user_id: uuid.UUID = Field(examples=[str(uuid.uuid4())])

    created_at: datetime = Field(examples=["2022-02-24T07:59:03.913Z"])
    updated_at: datetime = Field(examples=["2022-02-24T07:59:03.913Z"])


class PrivateUser(UserResponse):
    model_config = ConfigDict(from_attributes=True)
    password: str


class UserUpdate(BaseModel):
    username: str | None = Field(
        examples=["Jane Smith"], default=None, min_length=2, max_length=30
    )
    phone: str | None = Field(examples=["+380631112233"], default=None)


class TokenModel(BaseModel):
    access_token: str
    token_type: str = "bearer"

