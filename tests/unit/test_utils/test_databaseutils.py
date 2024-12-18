import pytest
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.user import User
from app.utils.database_utils import DatabaseUtils


def test_add_and_commit(db):
    """
    Test the add_and_commit method.
    """
    db_utils = DatabaseUtils(db)

    user = User(
        email="test_user@example.com",
        hashed_password="hashed_password",
        first_name="John",
        last_name="Doe",
        is_active=True
    )

    saved_user = db_utils.add_and_commit(user)

    # Validate that the user was saved
    assert saved_user.id is not None
    assert saved_user.email == "test_user@example.com"


def test_commit_and_refresh(db):
    """
    Test the commit_and_refresh method.
    """
    db_utils = DatabaseUtils(db)

    user = User(
        email="refresh_test@example.com",
        hashed_password="hashed_password",
        first_name="Jane",
        last_name="Smith",
        is_active=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Update an attribute and commit
    user.first_name = "Updated"
    updated_user = db_utils.commit_and_refresh(user)

    assert updated_user.first_name == "Updated"


def test_get_by_id_success(db):
    """
    Test the get_by_id method with a valid ID.
    """
    db_utils = DatabaseUtils(db)

    user = User(
        email="getbyid_test@example.com",
        hashed_password="hashed_password",
        first_name="Chris",
        last_name="Evans",
        is_active=True
    )
    saved_user = db_utils.add_and_commit(user)

    retrieved_user = db_utils.get_by_id(User, saved_user.id)

    assert retrieved_user.id == saved_user.id
    assert retrieved_user.email == "getbyid_test@example.com"


def test_get_by_id_not_found(db):
    """
    Test the get_by_id method with an invalid ID.
    """
    db_utils = DatabaseUtils(db)

    with pytest.raises(HTTPException, match="User with ID 1 not found"):
        db_utils.get_by_id(User, 1)


def test_find_or_404(db):
    """
    Test the find_or_404 method.
    """
    db_utils = DatabaseUtils(db)

    user = User(
        email="findor404_test@example.com",
        hashed_password="hashed_password",
        first_name="Mark",
        last_name="Ruffalo",
        is_active=True
    )
    db_utils.add_and_commit(user)

    retrieved_user = db_utils.find_or_404(User, email="findor404_test@example.com")
    assert retrieved_user.email == "findor404_test@example.com"

    with pytest.raises(HTTPException, match="User with email=nonexistent@example.com not found"):
        db_utils.find_or_404(User, email="nonexistent@example.com")


def test_delete_and_commit(db):
    """
    Test the delete_and_commit method.
    """
    db_utils = DatabaseUtils(db)

    user = User(
        email="delete_test@example.com",
        hashed_password="hashed_password",
        first_name="Paul",
        last_name="Rudd",
        is_active=True
    )
    saved_user = db_utils.add_and_commit(user)

    db_utils.delete_and_commit(saved_user)

    with pytest.raises(HTTPException, match="User with ID .* not found"):
        db_utils.get_by_id(User, saved_user.id)


def test_find_and_update(db):
    """
    Test the find_and_update method.
    """
    db_utils = DatabaseUtils(db)

    user = User(
        email="update_test@example.com",
        hashed_password="hashed_password",
        first_name="Brie",
        last_name="Larson",
        is_active=True
    )
    saved_user = db_utils.add_and_commit(user)

    updated_user = db_utils.find_and_update(User, saved_user.id, {"first_name": "Updated"})

    assert updated_user.first_name == "Updated"
    assert updated_user.id == saved_user.id


def test_bulk_update(db):
    """
    Test the bulk_update method.
    """
    db_utils = DatabaseUtils(db)

    user1 = User(
        email="bulk1@example.com",
        hashed_password="hashed_password",
        first_name="First",
        last_name="User",
        is_active=True
    )
    user2 = User(
        email="bulk2@example.com",
        hashed_password="hashed_password",
        first_name="Second",
        last_name="User",
        is_active=False
    )
    db_utils.add_and_commit(user1)
    db_utils.add_and_commit(user2)

    updates = [
        {"id": user1.id, "first_name": "UpdatedFirst"},
        {"id": user2.id, "first_name": "UpdatedSecond", "is_active": True}
    ]
    updated_users = db_utils.bulk_update(User, updates)

    assert updated_users[0].first_name == "UpdatedFirst"
    assert updated_users[1].first_name == "UpdatedSecond"
    assert updated_users[1].is_active is True
