from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.dependency import get_current_user
from app.services.job_history_service import JobHistoryService
from app.schemas.job_history import JobHistoryCreate, JobHistoryUpdate, JobHistoryResponse
from app.models.user import User

router = APIRouter()


@router.get("/job-history", response_model=List[JobHistoryResponse])
async def get_user_jobs(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all job history entries for a specific user.
    """
    job_history_service = JobHistoryService(db)
    return job_history_service.get_user_jobs(user_id)


@router.post("/create-job-history", response_model=JobHistoryResponse, status_code=201)
async def create_job_history(
    job_history_data: JobHistoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new job history entry for the user.
    """
    job_history_service = JobHistoryService(db)
    return job_history_service.create_job_history(job_history_data)


@router.put("/edit-job-history/{job_history_id}", response_model=JobHistoryResponse)
async def edit_job_history(
    job_history_id: int,
    job_data: JobHistoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a job history entry by ID.
    """
    job_history_service = JobHistoryService(db)
    return job_history_service.edit_job_history(job_history_id, job_data)


@router.delete("/delete-job-history/{job_history_id}")
async def delete_job_history(
    job_history_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a job history entry by ID.
    """
    job_history_service = JobHistoryService(db)
    return job_history_service.delete_job_history(job_history_id)
