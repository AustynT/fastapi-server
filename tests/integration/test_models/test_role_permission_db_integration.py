"""
Integration Tests for RolePermission Model

These tests validate the RolePermission model's behavior, relationships,
and constraints by interacting with the database.
"""

import pytest
from sqlalchemy.exc import IntegrityError
from app.models.role_permission import RolePermission
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

@pytest.fixture
def sample_user(db):
    """Creates a sample user."""
    user = User(email="test_user@example.com", hashed_password="hashed123", first_name="Test", last_name="User")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def sample_role(db):
    """Creates a sample role."""
    role = Role(name="admin", description="Administrator role")
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

@pytest.fixture
def sample_permission(db):
    """Creates a sample permission."""
    permission = Permission(name="read_data", description="Permission to read data")
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

def test_create_role_permission(db, sample_user, sample_role, sample_permission):
    """
    Test creating a RolePermission entry in the database.
    """
    role_permission = RolePermission(
        user_id=sample_user.id,
        role_id=sample_role.id,
        permission_id=sample_permission.id
    )
    db.add(role_permission)
    db.commit()
    db.refresh(role_permission)

    assert role_permission.id is not None
    assert role_permission.user_id == sample_user.id
    assert role_permission.role_id == sample_role.id
    assert role_permission.permission_id == sample_permission.id

def test_role_permission_unique_constraint(db, sample_user, sample_role, sample_permission):
    """
    Test that the UniqueConstraint (user_id, role_id, permission_id) is enforced.
    """
    role_permission1 = RolePermission(
        user_id=sample_user.id,
        role_id=sample_role.id,
        permission_id=sample_permission.id
    )
    db.add(role_permission1)
    db.commit()

    # Attempt to add a duplicate entry
    role_permission2 = RolePermission(
        user_id=sample_user.id,
        role_id=sample_role.id,
        permission_id=sample_permission.id
    )
    db.add(role_permission2)

    with pytest.raises(IntegrityError, match="uq_role_permission"):
        db.commit()
    db.rollback()

def test_optional_permission_id(db, sample_user, sample_role):
    """
    Test creating a RolePermission without a permission_id.
    """
    role_permission = RolePermission(
        user_id=sample_user.id,
        role_id=sample_role.id,
        permission_id=None
    )
    db.add(role_permission)
    db.commit()
    db.refresh(role_permission)

    assert role_permission.id is not None
    assert role_permission.permission_id is None
