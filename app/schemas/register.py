from pydantic import BaseModel, EmailStr, Field
from app.schemas.token import TokenResponse

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=50)
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)

class RegisterResponse(BaseModel):
    """
    Schema for user registration responses.
    """
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    created_at: str
    updated_at: str
    token: TokenResponse
