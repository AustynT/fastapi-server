from datetime import datetime, timedelta, timezone
from app.models.token import Token


def test_token_model_initialization():
    """
    Test that a Token object initializes with the correct attributes.
    """
    now = datetime.now(timezone.utc)
    token = Token(
        token="access123",
        refresh_token="refresh123",
        user_id=1,
        expires_at=now + timedelta(minutes=15),
        refresh_expires_at=now + timedelta(days=7),
        is_blacklisted=False
    )

    assert token.token == "access123"
    assert token.refresh_token == "refresh123"
    assert token.user_id == 1
    assert token.is_blacklisted is False
    assert token.expires_at > now
    assert token.refresh_expires_at > now


def test_token_model_blacklisted_flag():
    """
    Test the is_blacklisted flag works correctly.
    """
    token = Token(
        token="access123",
        refresh_token="refresh123",
        user_id=1,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
        refresh_expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        is_blacklisted=True
    )

    assert token.is_blacklisted is True
