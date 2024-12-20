from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing_extensions import Annotated
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str = Field(..., max_length=50, min_length=3)
    last_name: str = Field(..., max_length=50, min_length=3)
    created_at: datetime
    updated_at: datetime

    # Explicit validators for first_name and last_name
    @field_validator("first_name")
    def validate_first_name_length(cls, value):
        if len(value) > 50:
            raise ValueError("first_name must not exceed 50 characters")
        return value

    @field_validator("last_name")
    def validate_last_name_length(cls, value):
        if len(value) > 50:
            raise ValueError("last_name must not exceed 50 characters")
        return value

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
            }
        }
    )
