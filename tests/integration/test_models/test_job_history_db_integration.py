from datetime import datetime, timezone
import pytest
from app.models.job_history import JobHistory
from app.models.user import User


def strip_timezone(dt):
    """Helper to make datetime naive by stripping timezone."""
    return dt.replace(tzinfo=None)


@pytest.mark.usefixtures("db")
def test_create_and_retrieve_job_history(db):
    """
    Test creating and retrieving a JobHistory record in the database.
    """
    # Create a user with all required fields
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        first_name="John",
        last_name="Doe",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create a job history for the user
    start_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
    job_history = JobHistory(
        user_id=user.id,
        location="Remote",
        description="Engineer",
        is_active=True,
        start_date=start_date,
        end_date=None
    )
    db.add(job_history)
    db.commit()
    db.refresh(job_history)

    # Validate the job history record
    assert job_history.id is not None
    assert job_history.location == "Remote"
    assert job_history.description == "Engineer"
    assert job_history.is_active is True
    assert strip_timezone(job_history.start_date) == strip_timezone(start_date)
    assert job_history.end_date is None


@pytest.mark.usefixtures("db")
def test_job_history_with_end_date(db):
    """
    Test creating a JobHistory record with an end_date.
    """
    # Create a user with all required fields
    user = User(
        email="test2@example.com",
        hashed_password="hashed_password",
        first_name="Jane",
        last_name="Smith",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create a job history with an end date
    start_date = datetime(2022, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
    job_history = JobHistory(
        user_id=user.id,
        location="On-Site",
        description="Manager",
        is_active=False,
        start_date=start_date,
        end_date=end_date
    )
    db.add(job_history)
    db.commit()
    db.refresh(job_history)

    # Validate the job history record
    assert job_history.id is not None
    assert job_history.location == "On-Site"
    assert job_history.description == "Manager"
    assert job_history.is_active is False
    assert strip_timezone(job_history.start_date) == strip_timezone(start_date)
    assert strip_timezone(job_history.end_date) == strip_timezone(end_date)
