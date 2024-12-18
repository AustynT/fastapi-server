from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from app.schemas.token import TokenResponse


class RegisterRequest(BaseModel):
    """
    Schema for user registration requests.
    """
    email: EmailStr = Field(..., description="The email address of the user.")
    password: Annotated[str, Field(min_length=6, max_length=50)] = Field(
        ..., description="Password with a minimum length of 6 and a maximum of 50 characters."
    )
    first_name: Annotated[str, Field(max_length=50)] = Field(..., description="The user's first name.")
    last_name: Annotated[str, Field(max_length=50)] = Field(..., description="The user's last name.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "securepassword",
                "first_name": "John",
                "last_name": "Doe",
            }
        }
    )


class RegisterResponse(BaseModel):
    """
    Schema for user registration responses.
    """
    id: int = Field(..., description="The unique identifier of the user.")
    email: EmailStr = Field(..., description="The email address of the user.")
    first_name: str = Field(..., description="The user's first name.")
    last_name: str = Field(..., description="The user's last name.")
    created_at: datetime = Field(..., description="The timestamp when the user was created.")
    updated_at: datetime = Field(..., description="The timestamp when the user was last updated.")
    token: TokenResponse = Field(..., description="The access and refresh token details.")

    model_config = ConfigDict(
        from_attributes=True,  # Replaces `orm_mode`
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "user@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "created_at": "2023-12-01T00:00:00Z",
                "updated_at": "2023-12-01T00:00:00Z",
                "token": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                },
            }
        }
    )
