import pytest
from sqlalchemy.exc import IntegrityError
from app.models.permission import Permission

@pytest.fixture
def permission_data():
    """Provides sample permission data."""
    return {"name": "read_users", "description": "Permission to read user data"}

def test_create_permission(db, permission_data):
    """
    Test creating a permission in the database.
    """
    permission = Permission(**permission_data)
    db.add(permission)
    db.commit()
    db.refresh(permission)

    assert permission.id is not None
    assert permission.name == "read_users"
    assert permission.description == "Permission to read user data"


def test_permission_name_uniqueness(db, permission_data):
    """
    Test that the 'name' field enforces a uniqueness constraint.
    """
    # Create the first permission
    permission1 = Permission(**permission_data)
    db.add(permission1)
    db.commit()

    # Attempt to create a second permission with the same name
    permission2 = Permission(**permission_data)
    db.add(permission2)

    with pytest.raises(IntegrityError, match="uq_permission_name"):
        db.commit()
    db.rollback()


def test_permission_relationship(db, permission_data):
    """
    Test that the permission has a relationship with RolePermission.
    """
    permission = Permission(**permission_data)
    db.add(permission)
    db.commit()
    db.refresh(permission)

    # The permission should initially have no role_permissions
    assert permission.role_permissions == []
