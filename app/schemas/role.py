from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class RoleBase(BaseModel):
    """
    Shared fields for Role schema.
    """
    name: str = Field(..., max_length=50, description="The name of the role.")
    description: Optional[str] = Field(None, max_length=255, description="A brief description of the role.")

class RoleCreate(RoleBase):
    """
    Fields required for creating a new role.
    """
    pass

class RoleUpdate(BaseModel):
    """
    Fields that can be updated for a role.
    """
    name: Optional[str] = Field(None, max_length=50, description="The updated name of the role.")
    description: Optional[str] = Field(None, max_length=255, description="The updated description of the role.")

class RoleResponse(RoleBase):
    """
    Fields returned in the API response for a single role.
    """
    role_id: int = Field(..., description="The unique identifier for the role.")

    model_config = ConfigDict(
        from_attributes=True,  # Ensures the model can be populated from ORM objects
        json_schema_extra={
            "example": {
                "role_id": 1,
                "name": "Admin",
                "description": "Administrator with full access.",
            }
        },
    )

class RoleListResponse(BaseModel):
    """
    Fields returned in the API response for a list of roles.
    """
    roles: List[RoleResponse]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "roles": [
                    {"role_id": 1, "name": "Admin", "description": "Administrator with full access."},
                    {"role_id": 2, "name": "Editor", "description": "Editor with limited access."},
                ]
            }
        },
    )
