from app.services.base_service import BaseService
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate
from fastapi import HTTPException

class RoleService(BaseService):
    def get_all_roles(self):
        """
        Retrieve all roles from the database.
        """
        return self._database.get_all(Role)

    def get_role_by_id(self, role_id: int):
        """
        Retrieve a single role by its ID.
        """
        role = self._database.get_by_id(Role, role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role

    def create_role(self, role_data: RoleCreate):
        """
        Create a new role and save it to the database.
        """
        new_role = Role(**role_data.dict())
        return self._database.add_and_commit(new_role)

    def update_role(self, role_id: int, updated_data: RoleUpdate):
        """
        Update an existing role by its ID.
        """
        role = self._database.get_by_id(Role, role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        for key, value in updated_data.dict(exclude_unset=True).items():
            setattr(role, key, value)
        return self._database.commit_and_refresh(role)

    def delete_role(self, role_id: int):
        """
        Delete a role by its ID.
        """
        role = self._database.get_by_id(Role, role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        self._database.delete_and_commit(role)
        return {"message": "Role deleted successfully"}
