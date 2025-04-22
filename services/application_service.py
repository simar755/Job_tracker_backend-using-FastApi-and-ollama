# services/application_service.py
from sqlalchemy.orm import Session
from models.application_model import Application
from repository import application_repository
from fastapi import HTTPException, status

# Service function to create a new job application
def create_application(db: Session, job_id: int, user_id: int, resume: str):
    # Create a new Application model instance with the provided job ID and user ID
    app = Application(job_id=job_id, user_id=user_id)
    # Use the repository function to apply for the job and return the created application
    return application_repository.apply_job(db, app, resume)

# Service function to change the status of an existing job application
def change_application_status(db: Session, application_id: int, status: str):
    # Define a list of valid application statuses
    valid_statuses = ["applied", "interviewing", "offered", "rejected"]
    # Check if the provided status is valid
    if status not in valid_statuses:
        # Raise an HTTPException with a 400 Bad Request status if the status is invalid
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")
    # Use the repository function to update the application status and return the updated application
    return application_repository.update_application_status(db, application_id, status)