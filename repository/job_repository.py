# repository/job_repository.py
from sqlalchemy.orm import Session
from models.job_model import Job

# Repository function to create a new job listing
def create_job(db: Session, job: Job):
    # Add the job object to the database session
    db.add(job)
    # Commit the changes to the database
    db.commit()
    # Refresh the job object to get the updated state from the database
    db.refresh(job)
    # Return the created job object
    return job

# Repository function to retrieve all job listings
def get_all_jobs(db: Session):
    # Query the database for all job objects and return them as a list
    return db.query(Job).all()

# Repository function to update an existing job listing
def update_job(db: Session, job_id: int, title: str, description: str):
    # Query the database for the job with the given ID
    job = db.query(Job).filter(Job.id == job_id).first()
    # Check if the job exists
    if job:
        # Update the job's title and description
        job.title = title
        job.description = description
        # Commit the changes to the database
        db.commit()
    # Return the updated job object (or None if the job was not found)
    return job

# Repository function to delete a job listing
def delete_job(db: Session, job_id: int):
    # Query the database for the job with the given ID
    job = db.query(Job).filter(Job.id == job_id).first()
    # Check if the job exists
    if job:
        # Delete the job object from the database session
        db.delete(job)
        # Commit the changes to the database
        db.commit()