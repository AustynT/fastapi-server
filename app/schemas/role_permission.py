from pydantic import BaseModel, Field, ConfigDict
from typing import List
from app.schemas.role import RoleResponse
from app.schemas.permission import PermissionResponse

class RolePermissionBase(BaseModel):
    """
    Shared fields for RolePermission schema.
    """
    role_id: int = Field(..., description="The unique identifier for the role.")
    permission_id: int = Field(..., description="The unique identifier for the permission.")

class RolePermissionCreate(RolePermissionBase):
    """
    Fields required for creating a new role-permission association.
    """
    pass

class RolePermissionResponse(BaseModel):
    """
    Fields returned in the API response for a single role-permission association.
    """
    id: int = Field(..., description="The unique identifier for the role-permission association.")
    role: RoleResponse = Field(..., description="The role associated with this permission.")
    permission: PermissionResponse = Field(..., description="The permission associated with this role.")

    model_config = ConfigDict(
        from_attributes=True,  # Ensures the model can be populated from ORM objects
        json_schema_extra={
            "example": {
                "id": 1,
                "role": {
                    "role_id": 1,
                    "name": "Admin",
                    "description": "Administrator with full access."
                },
                "permission": {
                    "permission_id": 2,
                    "name": "Write",
                    "description": "Permission to write resources."
                }
            }
        },
    )

class RolePermissionListResponse(BaseModel):
    """
    Fields returned in the API response for a list of role-permission associations.
    """
    role_permissions: List[RolePermissionResponse]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "role_permissions": [
                    {
                        "id": 1,
                        "role": {
                            "role_id": 1,
                            "name": "Admin",
                            "description": "Administrator with full access."
                        },
                        "permission": {
                            "permission_id": 2,
                            "name": "Write",
                            "description": "Permission to write resources."
                        }
                    },
                    {
                        "id": 2,
                        "role": {
                            "role_id": 2,
                            "name": "Editor",
                            "description": "Editor with limited access."
                        },
                        "permission": {
                            "permission_id": 3,
                            "name": "Delete",
                            "description": "Permission to delete resources."
                        }
                    }
                ]
            }
        },
    )