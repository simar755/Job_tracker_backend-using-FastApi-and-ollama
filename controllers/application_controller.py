from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.application_model import Application
from dependencies import get_current_user
from fastapi import APIRouter, HTTPException, Query
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import Dict
# Create an APIRouter instance for application-related endpoints
router = APIRouter(prefix="/applications", tags=["Applications"])

# Endpoint to apply for a job
@router.post("/")
def apply_to_job(job_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Create a new Application instance with the job ID and user ID from the current_user dependency
    application = Application(job_id=job_id, user_id=current_user['user_id'])
    # Add the application to the database session
    db.add(application)
    # Commit the changes to the database
    db.commit()
    # Return a success message
    return {"msg": "Application submitted"}


# Endpoint to update the status of an application
@router.put("/status/{application_id}")
def update_status(application_id: int, new_status: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if the current user's role is authorized to update application statuses
    if current_user["role"] not in ["admin", "hr"]:
        # Raise an HTTPException with a 403 Forbidden status if not authorized
        raise HTTPException(status_code=403, detail="Unauthorized")
    # Define a list of valid application statuses
    valid_statuses = ["Interviewing", "Offered", "Rejected"]
    # Check if the provided new status is valid
    if new_status not in valid_statuses:
        # Raise an HTTPException with a 400 Bad Request status if the status is invalid
        raise HTTPException(status_code=400, detail="Invalid status")
    # Query the database for the application with the given ID
    app = db.query(Application).filter(Application.id == application_id).first()
    # Check if the application exists
    if not app:
        # Raise an HTTPException with a 404 Not Found status if the application is not found
        raise HTTPException(status_code=404, detail="Application not found")
    # Update the application's status with the new status
    app.status = new_status
    # Commit the changes to the database
    db.commit()
    # Return a success message
    return {"msg": "Status updated"}