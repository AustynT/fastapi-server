import pytest
from sqlalchemy.exc import IntegrityError
from app.models.user import User

def test_create_user(db):
    """
    Test creating a user in the database.
    """
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        first_name="John",
        last_name="Doe",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.hashed_password == "hashed_password"

def test_unique_email_constraint(db):
    """
    Test that creating users with duplicate emails raises an IntegrityError.
    """
    user1 = User(
        email="test@example.com",
        hashed_password="hashed_password1",
        first_name="John",
        last_name="Doe",
    )
    db.add(user1)
    db.commit()

    user2 = User(
        email="test@example.com",  # Duplicate email
        hashed_password="hashed_password2",
        first_name="Jane",
        last_name="Smith",
    )
    db.add(user2)

    with pytest.raises(IntegrityError):
        db.commit()

def test_user_cleanup(db):
    """
    Ensure the database is clean after the test.
    """
    users = db.query(User).all()
    assert len(users) == 0  # Ensure no users exist

@pytest.mark.parametrize(
    "email, hashed_password, first_name, last_name",
    [
        ("test1@example.com", "hashed1", "John", "Doe"),
        ("test2@example.com", "hashed2", "Jane", "Smith"),
    ],
)
def test_create_user_parametrized(db, email, hashed_password, first_name, last_name):
    """
    Test creating multiple users using parametrization.
    """
    user = User(
        email=email,
        hashed_password=hashed_password,
        first_name=first_name,
        last_name=last_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.email == email
    assert user.first_name == first_name
    assert user.last_name == last_name
