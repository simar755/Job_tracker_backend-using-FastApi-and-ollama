from sqlalchemy.orm import Session
from models.job_model import Job
from repository import job_repository

# Service function to add a new job listing to the database
def add_job(db: Session, title: str, description: str):
    # Create a new Job model instance with the provided title and description
    new_job = Job(title=title, description=description)
    # Use the repository function to create the job in the database and return the created job
    return job_repository.create_job(db, new_job)

# Service function to retrieve all job listings from the database
def get_jobs(db: Session):
    # Use the repository function to get all jobs from the database and return them
    return job_repository.get_all_jobs(db)

# Service function to edit an existing job listing in the database
def edit_job(db: Session, job_id: int, title: str, description: str):
    # Use the repository function to update the job with the provided ID, title, and description
    return job_repository.update_job(db, job_id, title, description)

# Service function to remove a job listing from the database
def remove_job(db: Session, job_id: int):
    # Use the repository function to delete the job with the provided ID from the database
    job_repository.delete_job(db, job_id)