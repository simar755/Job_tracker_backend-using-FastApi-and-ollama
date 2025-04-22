# models/application_model.py
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Application(Base):
    __tablename__ = 'applications'
    # Primary key column: unique integer identifier for each application
    id = Column(Integer, primary_key=True, index=True)
    # Foreign key referencing the 'jobs' table: job ID for the application
    job_id = Column(Integer, ForeignKey("jobs.id"))
    # Foreign key referencing the 'users' table: user ID for the application
    user_id = Column(Integer, ForeignKey("users.id"))
    # Application status (string, default is "Applied")
    status = Column(String, default="Applied")
    # Link to the user's resume (string)
    resume = Column(String)