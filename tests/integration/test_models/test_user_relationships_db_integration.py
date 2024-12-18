"""
Integration tests for User model relationships with Token, RolePermission, and JobHistory.
"""

from datetime import datetime, timedelta, timezone
import pytest
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User
from app.models.token import Token
from app.models.role_permission import RolePermission
from app.models.job_history import JobHistory


def strip_timezone(dt):
    """Helper to make datetime naive by stripping timezone."""
    return dt.replace(tzinfo=None)


@pytest.fixture
def sample_user(db):
    """Creates a sample user."""
    user = User(
        email="test_user_relationships@example.com",
        hashed_password="hashed_password",
        first_name="John",
        last_name="Doe",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_user_token_relationship(db, sample_user):
    """
    Test the relationship between User and Token.
    """
    now = datetime.now(timezone.utc)

    # Create tokens for the user
    token1 = Token(
        token="access_token_1",
        refresh_token="refresh_token_1",
        user_id=sample_user.id,
        expires_at=now + timedelta(minutes=15),
        refresh_expires_at=now + timedelta(days=7),
        is_blacklisted=False
    )
    token2 = Token(
        token="access_token_2",
        refresh_token="refresh_token_2",
        user_id=sample_user.id,
        expires_at=now + timedelta(minutes=15),
        refresh_expires_at=now + timedelta(days=7),
        is_blacklisted=False
    )

    db.add_all([token1, token2])
    db.commit()

    # Refresh the user and validate tokens
    db.refresh(sample_user)
    assert len(sample_user.tokens) == 2
    assert sample_user.tokens[0].token == "access_token_1"
    assert sample_user.tokens[1].token == "access_token_2"


def test_user_role_permission_relationship(db, sample_user):
    """
    Test the relationship between User and RolePermission.
    """
    # Create roles and permissions
    role1 = Role(name="Admin", description="Administrator role")
    role2 = Role(name="Editor", description="Editor role")
    permission1 = Permission(name="read_data", description="Can read data")
    permission2 = Permission(name="write_data", description="Can write data")

    db.add_all([role1, role2, permission1, permission2])
    db.commit()

    # Create role permissions for the user
    role_permission1 = RolePermission(user_id=sample_user.id, role_id=role1.id, permission_id=permission1.id)
    role_permission2 = RolePermission(user_id=sample_user.id, role_id=role2.id, permission_id=permission2.id)

    db.add_all([role_permission1, role_permission2])
    db.commit()

    # Refresh the user and validate role permissions
    db.refresh(sample_user)
    assert len(sample_user.role_permissions) == 2
    assert sample_user.role_permissions[0].role_id == role1.id
    assert sample_user.role_permissions[0].permission_id == permission1.id
    assert sample_user.role_permissions[1].role_id == role2.id
    assert sample_user.role_permissions[1].permission_id == permission2.id



def test_user_job_history_relationship(db, sample_user):
    """
    Test the relationship between User and JobHistory.
    """
    now = datetime.now(timezone.utc)

    # Create job history entries for the user
    job1 = JobHistory(
        user_id=sample_user.id,
        location="New York",
        description="Software Engineer",
        is_active=False,
        start_date=now - timedelta(days=365),
        end_date=now - timedelta(days=180)
    )
    job2 = JobHistory(
        user_id=sample_user.id,
        location="San Francisco",
        description="Senior Software Engineer",
        is_active=True,
        start_date=now - timedelta(days=90),
        end_date=None
    )

    db.add_all([job1, job2])
    db.commit()

    # Refresh the user and validate job histories
    db.refresh(sample_user)
    assert len(sample_user.job_histories) == 2
    assert sample_user.job_histories[0].location == "New York"
    assert sample_user.job_histories[1].location == "San Francisco"
    assert strip_timezone(sample_user.job_histories[0].start_date) == strip_timezone(now - timedelta(days=365))
    assert strip_timezone(sample_user.job_histories[0].end_date) == strip_timezone(now - timedelta(days=180))
