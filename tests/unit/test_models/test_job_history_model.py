from datetime import datetime, timedelta, timezone
import pytest
from app.models.job_history import JobHistory


def test_validate_start_date():
    """
    Test that start_date cannot be in the future.
    """
    job = JobHistory(location="Remote", description="Engineer", is_active=True)
    
    # Valid start_date (past)
    valid_start_date = datetime.now(timezone.utc) - timedelta(days=1)
    job.start_date = valid_start_date
    assert job.start_date == valid_start_date

    # Invalid start_date (future)
    with pytest.raises(ValueError, match="start_date cannot be in the future"):
        job.start_date = datetime.now(timezone.utc) + timedelta(days=1)


def test_validate_end_date():
    """
    Test that end_date must be after start_date.
    """
    job = JobHistory(location="Remote", description="Engineer", is_active=True)
    job.start_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
    
    # Valid end_date
    valid_end_date = datetime(2023, 12, 31, tzinfo=timezone.utc)
    job.end_date = valid_end_date
    assert job.end_date == valid_end_date

    # Invalid end_date (before start_date)
    with pytest.raises(ValueError, match="end_date must be after start_date"):
        job.end_date = datetime(2022, 12, 31, tzinfo=timezone.utc)


def test_validate_location():
    """
    Test that location cannot be empty or only whitespaces.
    """


    
    job = JobHistory(description="Engineer", is_active=True, start_date=datetime.now(timezone.utc))

    # Invalid location
    with pytest.raises(ValueError, match=r"(?i)location.*empty.*whitespace"):
        job.location = "  "  # Only whitespace

    # Valid location
    job.location = "Remote"
    assert job.location == "Remote"



def test_is_current():
    """
    Test the is_current property logic for active and inactive jobs.
    """
    job = JobHistory(location="Remote", description="Engineer", is_active=True)
    job.start_date = datetime.now(timezone.utc) - timedelta(days=10)

    # No end_date - job is current
    job.end_date = None
    assert job.is_current is True

    # End_date in the past - job is not current
    job.end_date = datetime.now(timezone.utc) - timedelta(days=1)
    assert job.is_current is False

    # End_date in the future - job is current
    job.end_date = datetime.now(timezone.utc) + timedelta(days=1)
    assert job.is_current is True
