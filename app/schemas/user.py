from pydantic import BaseModel, EmailStr, ConfigDict
from typing_extensions import Annotated
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: Annotated[str, {"max_length": 50}]  # Example of length constraint
    last_name: Annotated[str, {"max_length": 50}]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,  # Replaces `orm_mode`
        json_schema_extra={    # Replaces `schema_extra`
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
