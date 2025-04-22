# repository/application_repository.py
from sqlalchemy.orm import Session
from models.application_model import Application

# Repository function to apply for a job
def apply_job(db: Session, application: Application, resume: str):
    # Set the resume link for the application
    application.resume = resume
    # Add the application object to the database session
    db.add(application)
    # Commit the changes to the database
    db.commit()
    # Refresh the application object to get the updated state from the database
    db.refresh(application)
    # Return the created application object
    return {
        "message": "Application submitted successfully",
        "application_id": application.id,
        "resume_saved_at": application.resume
    }


# Repository function to update the status of an application
def update_application_status(db: Session, application_id: int, status: str):
    # Query the database for the application with the given ID
    app = db.query(Application).filter(Application.id == application_id).first()
    # Check if the application exists
    if app:
        # Update the application's status
        app.status = status
        # Commit the changes to the database
        db.commit()
        # Refresh the application object to get the updated state from the database
        db.refresh(app)
    # Return the updated application object (or None if the application was not found)
    return app
