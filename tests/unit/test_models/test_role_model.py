import pytest
from sqlalchemy.exc import IntegrityError
from app.models.role import Role

@pytest.fixture
def role_data():
    """Provides sample role data."""
    return {"name": "Admin", "description": "Administrator role"}

def test_create_role(db, role_data):
    """
    Test creating a role in the database.
    """
    role = Role(**role_data)
    db.add(role)
    db.commit()
    db.refresh(role)

    assert role.id is not None
    assert role.name == "Admin"
    assert role.description == "Administrator role"


def test_role_name_uniqueness(db, role_data):
    """
    Test that the 'name' field enforces a uniqueness constraint.
    """
    # Create the first role
    role1 = Role(**role_data)
    db.add(role1)
    db.commit()

    # Attempt to create a second role with the same name
    role2 = Role(**role_data)
    db.add(role2)

    with pytest.raises(IntegrityError, match="uq_role_name"):
        db.commit()
    db.rollback()


def test_role_relationship(db, role_data):
    """
    Test that the role has a relationship with RolePermission.
    """
    role = Role(**role_data)
    db.add(role)
    db.commit()
    db.refresh(role)

    # The role should initially have no role_permissions
    assert role.role_permissions == []
