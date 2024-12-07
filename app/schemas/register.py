from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=50)
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)

class RegisterResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    created_at: str
    updated_at: str
    access_token: str  # Include the token in the response
    token_type: str
