from datetime import datetime, timedelta, timezone
import pytest
from app.models.token import Token
from app.models.user import User


@pytest.fixture
def sample_user(db):
    """
    Fixture to create a sample user.
    """
    user = User(email="test_user@example.com", hashed_password="hashed123", first_name="Test", last_name="User")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_delete_expired_tokens(db, sample_user):
    """
    Test the delete_expired_tokens method to remove expired tokens from the database.
    """
    now = datetime.now(timezone.utc)

    # Create valid and expired tokens
    valid_token = Token(
        token="valid123",
        refresh_token="refresh_valid123",
        user_id=sample_user.id,
        expires_at=now + timedelta(minutes=15),
        refresh_expires_at=now + timedelta(days=7),
        is_blacklisted=False
    )
    expired_token = Token(
        token="expired123",
        refresh_token="refresh_expired123",
        user_id=sample_user.id,
        expires_at=now - timedelta(minutes=15),
        refresh_expires_at=now - timedelta(days=7),
        is_blacklisted=False
    )

    db.add(valid_token)
    db.add(expired_token)
    db.commit()

    # Call the class method
    Token.delete_expired_tokens(db)

    # Validate that only the valid token remains
    remaining_tokens = db.query(Token).all()
    assert len(remaining_tokens) == 1
    assert remaining_tokens[0].token == "valid123"
