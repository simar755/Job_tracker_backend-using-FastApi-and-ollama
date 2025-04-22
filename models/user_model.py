# models/user_model.py
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'
    # Primary key column: unique integer identifier for each user
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # User's full name (string)
    name = Column(String)
    # User's email address (string, must be unique)
    email = Column(String, unique=True)
    # User's password (hashed string)
    password = Column(String)
    # User's role (string, either 'applicant' or 'admin')
    role = Column(String)