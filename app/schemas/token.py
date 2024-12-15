from pydantic import BaseModel

class TokenRequest(BaseModel):
    """
    Schema for requesting a new token (e.g., during refresh).
    """
    refresh_token: str


class TokenResponse(BaseModel):
    """
    Schema for returning tokens (e.g., after login or registration).
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
