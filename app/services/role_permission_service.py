from app.services.base_service import BaseService
from app.models.role_permission import RolePermission
from app.schemas.role_permission import RolePermissionCreate
from fastapi import HTTPException
from typing import List

class RolePermissionService(BaseService):
    def get_all_role_permissions(self):
        """
        Retrieve all role-permission associations from the database.
        """
        return self._database.get_all(RolePermission)

    def get_role_permission_by_id(self, role_permission_id: int):
        """
        Retrieve a single role-permission association by its ID.
        """
        role_permission = self._database.get_by_id(RolePermission, role_permission_id)
        if not role_permission:
            raise HTTPException(status_code=404, detail="Role-Permission association not found")
        return role_permission

    def get_permissions_for_role(self, role_id: int):
        """
        Retrieve all permissions associated with a specific role.
        """
        role_permissions = self._database.get_all(RolePermission)
        return [rp.permission for rp in role_permissions if rp.role_id == role_id]

    def create_role_permission(self, role_permission_data: RolePermissionCreate):
        """
        Create a new role-permission association and save it to the database.
        """
        new_role_permission = RolePermission(**role_permission_data.dict())
        return self._database.add_and_commit(new_role_permission)

    def add_multiple_permissions_to_role(self, role_id: int, permission_ids: List[int]):
        """
        Add multiple permissions to a role by creating role-permission associations.
        """
        new_role_permissions = [
            RolePermission(role_id=role_id, permission_id=permission_id) for permission_id in permission_ids
        ]
        self._database.bulk_add(new_role_permissions)
        self._database.commit()
        return {"message": f"Added {len(permission_ids)} permissions to role {role_id}"}

    def delete_role_permission(self, role_permission_id: int):
        """
        Delete a role-permission association by its ID.
        """
        role_permission = self._database.get_by_id(RolePermission, role_permission_id)
        if not role_permission:
            raise HTTPException(status_code=404, detail="Role-Permission association not found")
        self._database.delete_and_commit(role_permission)
        return {"message": "Role-Permission association deleted successfully"}
