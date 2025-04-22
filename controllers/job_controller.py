from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.job_model import Job
from database import get_db

# Create an APIRouter instance for job-related endpoints
router = APIRouter(prefix="/jobs", tags=["Jobs"])

# Endpoint to add a new job listing
@router.post("/")
def add_job(title: str, description: str, db: Session = Depends(get_db)):
    # Create a new Job instance with the provided title and description
    job = Job(title=title, description=description)
    # Add the job to the database session
    db.add(job)
    # Commit the changes to the database
    db.commit()
    # Return a success message
    return {"msg": "Job added"}

# Endpoint to update an existing job listing
@router.put("/{job_id}")
def update_job(job_id: int, title: str, description: str, db: Session = Depends(get_db)):
    # Query the database for the job with the given ID
    job = db.query(Job).get(job_id)
    # Update the job's title and description
    job.title = title
    job.description = description
    # Commit the changes to the database
    db.commit()
    # Return a success message
    return {"msg": "Job updated"}

# Endpoint to delete an existing job listing
@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    # Query the database to delete the job with the given ID
    db.query(Job).filter(Job.id == job_id).delete()
    # Commit the changes to the database
    db.commit()
    # Return a success message
    return {"msg": "Job deleted"}