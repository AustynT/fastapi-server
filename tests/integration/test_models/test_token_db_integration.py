from datetime import datetime, timedelta, timezone
import pytest
from app.models.token import Token
from app.models.user import User
from sqlalchemy.orm.session import make_transient

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


def test_create_valid_token(db, sample_user):
    """
    Test creating a valid token.
    """
    now = datetime.now(timezone.utc)

    # Create valid token
    valid_token = Token(
        token="valid123",
        refresh_token="refresh_valid123",
        user_id=sample_user.id,
        expires_at=now + timedelta(hours=1),
        refresh_expires_at=now + timedelta(days=7),
        is_blacklisted=False
    )
    db.add(valid_token)
    db.commit()

    # Validate the token in the database
    token = db.query(Token).filter_by(token="valid123").first()
    assert token is not None
    assert token.token == "valid123"
    assert not token.is_expired

def test_create_expired_token(db, sample_user):
    now = datetime.now(timezone.utc)

    # Attempt to create an expired token without skipping validation
    with pytest.raises(ValueError, match="expires_at must be set to a future time."):
        expired_token = Token(
            token="expired123",
            refresh_token="refresh_expired123",
            user_id=sample_user.id,
            expires_at=now - timedelta(hours=1),
            refresh_expires_at=now - timedelta(days=7),
            is_blacklisted=False
        )
        db.add(expired_token)
        db.commit()
