from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class PermissionBase(BaseModel):
    """
    Shared fields for Permission schema.
    """
    name: str = Field(..., max_length=50, description="The name of the permission.")
    description: Optional[str] = Field(None, max_length=255, description="A brief description of the permission.")

class PermissionCreate(PermissionBase):
    """
    Fields required for creating a new permission.
    """
    pass

class PermissionUpdate(BaseModel):
    """
    Fields that can be updated for a permission.
    """
    name: Optional[str] = Field(None, max_length=50, description="The updated name of the permission.")
    description: Optional[str] = Field(None, max_length=255, description="The updated description of the permission.")

class PermissionResponse(PermissionBase):
    """
    Fields returned in the API response for a single permission.
    """
    permission_id: int = Field(..., description="The unique identifier for the permission.")

    model_config = ConfigDict(
        from_attributes=True,  # Ensures the model can be populated from ORM objects
        json_schema_extra={
            "example": {
                "permission_id": 1,
                "name": "Read",
                "description": "Permission to read resources.",
            }
        },
    )

class PermissionListResponse(BaseModel):
    """
    Fields returned in the API response for a list of permissions.
    """
    permissions: List[PermissionResponse]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "permissions": [
                    {"permission_id": 1, "name": "Read", "description": "Permission to read resources."},
                    {"permission_id": 2, "name": "Write", "description": "Permission to write resources."},
                ]
            }
        },
    )
