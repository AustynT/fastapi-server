from app.services.base_service import BaseService
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate
from fastapi import HTTPException

class PermissionService(BaseService):
    def get_all_permissions(self):
        """
        Retrieve all permissions from the database.
        """
        return self._database.get_all(Permission)

    def get_permission_by_id(self, permission_id: int):
        """
        Retrieve a single permission by its ID.
        """
        permission = self._database.get_by_id(Permission, permission_id)
        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")
        return permission

    def create_permission(self, permission_data: PermissionCreate):
        """
        Create a new permission and save it to the database.
        """
        new_permission = Permission(**permission_data.dict())
        return self._database.add_and_commit(new_permission)

    def update_permission(self, permission_id: int, updated_data: PermissionUpdate):
        """
        Update an existing permission by its ID.
        """
        permission = self._database.get_by_id(Permission, permission_id)
        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")
        for key, value in updated_data.dict(exclude_unset=True).items():
            setattr(permission, key, value)
        return self._database.commit_and_refresh(permission)

    def delete_permission(self, permission_id: int):
        """
        Delete a permission by its ID.
        """
        permission = self._database.get_by_id(Permission, permission_id)
        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")
        self._database.delete_and_commit(permission)
        return {"message": "Permission deleted successfully"}
