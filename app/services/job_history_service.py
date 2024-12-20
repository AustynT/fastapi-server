from app.models.job_history import JobHistory
from app.schemas.job_history import JobHistoryCreate, JobHistoryUpdate
from app.services.base_service import BaseService
from fastapi import HTTPException, status
from datetime import datetime


class JobHistoryService(BaseService):
    def get_user_jobs(self, user_id: int):
        """
        Get all job history entries for a specific user.
        """
        jobs = self._database.find_or_404(JobHistory, user_id=user_id)
        return jobs

    def create_job_history(self, job_history_data: JobHistoryCreate):
        """
        Create a new job history entry.
        """
        new_job_history = JobHistory(**job_history_data.dict())
        return self._database.add_and_commit(new_job_history)

    def edit_job_history(self, job_history_id: int, job_data: JobHistoryUpdate):
        """
        Edit an existing job history entry.
        """
        job_history = self._database.get_by_id(JobHistory, job_history_id)

        for key, value in job_data.model_dump(exclude_unset=True).items():
            setattr(job_history, key, value)

        return self._database.commit_and_refresh(job_history)

    def delete_job_history(self, job_history_id: int):
        """
        Delete a job history entry by ID.
        """
        job_history = self._database.get_by_id(JobHistory, job_history_id)

        if job_history.end_date and job_history.end_date > datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete job history with an end date in the future",
            )

        self._database.delete_and_commit(job_history)
        return {"message": "Job history deleted successfully"}
