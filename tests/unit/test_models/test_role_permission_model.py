"""
Unit tests for RolePermission model.

Focus: Testing model initialization, attributes, and basic behavior without database.
"""

from app.models.role_permission import RolePermission


def test_role_permission_model_initialization():
    """
    Test that a RolePermission object initializes with the correct attributes.
    """
    role_permission = RolePermission(
        user_id=1,
        role_id=2,
        permission_id=3
    )

    assert role_permission.user_id == 1
    assert role_permission.role_id == 2
    assert role_permission.permission_id == 3
    assert role_permission.id is None  # ID will be assigned on database commit


def test_role_permission_optional_permission_id():
    """
    Test that RolePermission allows None for permission_id.
    """
    role_permission = RolePermission(
        user_id=1,
        role_id=2,
        permission_id=None
    )

    assert role_permission.user_id == 1
    assert role_permission.role_id == 2
    assert role_permission.permission_id is None


def test_role_permission_default_attributes():
    """
    Test that RolePermission defaults work as expected.
    """
    role_permission = RolePermission(user_id=1, role_id=2)

    assert role_permission.user_id == 1
    assert role_permission.role_id == 2
    assert role_permission.permission_id is None  # Default is None
