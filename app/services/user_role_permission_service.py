from app.services.base_service import BaseService
from app.services.role_permission_service import RolePermissionService
from app.models.role import Role
from app.models.user import User
from fastapi import HTTPException
from typing import List

class UserRolePermissionService(BaseService):
    def __init__(self, database, role_permission_service: RolePermissionService):
        super().__init__(database)
        self.role_permission_service = role_permission_service

    def get_user_role(self, user_id: int):
        """
        Retrieve the role assigned to a user.
        """
        user = self._database.get_by_id(User, user_id)
        return user.role

    def get_user_permissions(self, user_id: int):
        """
        Retrieve all permissions assigned to a user through their role.
        """
        user = self._database.get_by_id(User, user_id)
        if not user.role:
            raise HTTPException(status_code=404, detail=f"User {user_id} has no assigned role")
        return self.role_permission_service.get_permissions_for_role(user.role.id)

    def assign_role_to_user(self, user_id: int, role_id: int):
        """
        Assign a single role to a user.
        """
        user = self._database.get_by_id(User, user_id)
        role = self._database.get_by_id(Role, role_id)
        if user.role and user.role.id == role_id:
            raise HTTPException(status_code=400, detail=f"User {user_id} already has role {role_id}")
        user.role = role
        self._database.commit()
        return {"message": f"Role {role_id} assigned to user {user_id}"}

    def remove_role_from_user(self, user_id: int):
        """
        Remove the role from a user.
        """
        user = self._database.get_by_id(User, user_id)
        if user.role:
            user.role = None
            self._database.commit()
        else:
            raise HTTPException(status_code=400, detail=f"User {user_id} has no role to remove")
        return {"message": f"Role removed from user {user_id}"}

    def get_roles_permissions(self, role_id: int):
        """
        Retrieve all permissions associated with a role.
        """
        return self.role_permission_service.get_permissions_for_role(role_id)

    def add_permissions_to_role(self, role_id: int, permission_ids: List[int]):
        """
        Add multiple permissions to a role using RolePermissionService.
        """
        return self.role_permission_service.add_permissions_to_role(role_id, permission_ids)

    def get_user_role_permissions(self, user_id: int):
        """
        Retrieve the user's role and its permissions.
        """
        user = self._database.get_by_id(User, user_id)
        role = user.role
        if not role:
            raise HTTPException(status_code=404, detail=f"User {user_id} has no assigned role")
        permissions = self.role_permission_service.get_permissions_for_role(role.id)
        return {role.name: permissions}
