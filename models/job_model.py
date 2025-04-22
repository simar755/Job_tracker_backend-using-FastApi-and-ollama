from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel

# Pydantic model representing the base structure of a Job
class JobBase(BaseModel):
    id: int  # Job ID
    title: str  # Job title
    description: str  # Job description

# SQLAlchemy model representing the 'jobs' table in the database
class Job(Base):
    __tablename__ = 'jobs'  # Name of the table in the database
    id = Column(Integer, primary_key=True, index=True)  # Primary key, auto-indexed integer
    title = Column(String)  # Job title (string)
    description = Column(String)  # Job description (string)