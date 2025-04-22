# dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils.jwt_handler import verify_token
from database import SessionLocal
from typing import Generator

# OAuth2 password bearer scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependency to get the current user from the JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verify the JWT token and return the user payload
    return verify_token(token)

# Dependency to get a database session
def get_db() -> Generator:
    # Create a new database session
    db = SessionLocal()
    try:
        # Yield the database session to the request
        yield db
    finally:
        # Close the database session after the request is finished
        db.close()

