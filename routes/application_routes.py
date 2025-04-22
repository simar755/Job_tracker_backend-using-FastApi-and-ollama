from fastapi import APIRouter, Depends, HTTPException,UploadFile,File
from sqlalchemy.orm import Session
from services import application_service
from dependencies import get_db, get_current_user
from pydantic import BaseModel
import os
import shutil

# Define a Pydantic model for application requests
class ApplicationRequest(BaseModel):
    job_id: int
    resume_link: str

# Create an APIRouter instance for application-related endpoints
router = APIRouter(prefix="/applications", tags=["Applications"])
UPLOAD_DIR = "uploads/resumes"

# Ensure upload folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)
# Endpoint to apply for a job
@router.post("/apply")
def apply_to_job(job_id: int, resume: UploadFile = File(...), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)): #add resume_link
    # Save the uploaded file
    file_location = os.path.join(UPLOAD_DIR, resume.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    # Pass the saved file path to the service
    return application_service.create_application(
        db=db,
        job_id=job_id,
        user_id=current_user["user_id"],
        resume=file_location
    )
# Endpoint to update the status of an application
@router.put("/update-status/{application_id}")
def update_application_status(application_id: int, status: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Check if the current user's role is authorized to update application statuses
    if current_user["role"] not in ["hr", "admin"]:
        # Raise an HTTPException with a 403 Forbidden status if not authorized
        raise HTTPException(status_code=403, detail="Only HR/Admin can update status")
    # Call the application service to update the application status
    return application_service.change_application_status(db, application_id, status)