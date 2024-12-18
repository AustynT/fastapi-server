from pydantic import BaseModel, Field, ConfigDict


class TokenRequest(BaseModel):
    """
    Schema for requesting a new token (e.g., during refresh).
    """
    refresh_token: str = Field(..., description="The refresh token used to request a new access token.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            }
        }
    )


class TokenResponse(BaseModel):
    """
    Schema for returning tokens (e.g., after login or registration).
    """
    access_token: str = Field(..., description="The access token for authenticated API requests.")
    refresh_token: str = Field(..., description="The refresh token for generating new access tokens.")
    token_type: str = Field(default="bearer", description="The type of token being returned.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }
    )
