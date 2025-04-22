# routes/job_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services import job_service
from dependencies import get_db, get_current_user
from typing import List
from models.job_model import Job, JobBase  # Import Job and JobBase

# Create an APIRouter instance for job-related endpoints
router = APIRouter(prefix="/jobs", tags=["Jobs"])

# Endpoint to add a new job listing
@router.post("/add")
def add_job(title: str, description: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Check if the current user's role is authorized to add jobs
    if current_user["role"] not in ["hr", "admin"]:
        # Raise an HTTPException with a 403 Forbidden status if not authorized
        raise HTTPException(status_code=403, detail="Only HR/Admin can add jobs")
    # Call the job_service function to add the job and return the result
    return job_service.add_job(db, title, description)

# Endpoint to update an existing job listing
@router.put("/update/{job_id}")
def update_job(job_id: int, title: str, description: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Check if the current user's role is authorized to update jobs
    if current_user["role"] not in ["hr", "admin"]:
        # Raise an HTTPException with a 403 Forbidden status if not authorized
        raise HTTPException(status_code=403, detail="Only HR/Admin can update jobs")
    # Call the job_service function to update the job and return the result
    return job_service.edit_job(db, job_id, title, description)

# Endpoint to delete an existing job listing
@router.delete("/delete/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Check if the current user's role is authorized to delete jobs
    if current_user["role"] not in ["hr", "admin"]:
        # Raise an HTTPException with a 403 Forbidden status if not authorized
        raise HTTPException(status_code=403, detail="Only HR/Admin can delete jobs")
    # Call the job_service function to remove the job
    job_service.remove_job(db, job_id)
    # Return a success message
    return {"message": "Job deleted"}

# Endpoint to retrieve all job listings
@router.get("/", response_model=List[JobBase])  # Use JobBase for response model
def read_jobs(db: Session = Depends(get_db)):
    # Call the job_service function to get all jobs and return them
    return job_service.get_jobs(db)