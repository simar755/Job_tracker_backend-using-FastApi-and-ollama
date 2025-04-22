# services/user_service.py
from sqlalchemy.orm import Session
from models.user_model import User
from fastapi import HTTPException, status
from repository import user_repository

# Service function to update user details
def update_user_details(user_id: int, request_data: dict, db: Session):
    # Retrieve the user by ID using the repository function
    user = user_repository.get_user_by_id(user_id, db)

    # Check if the user exists
    if not user:
        # Raise an HTTPException with a 404 Not Found status if the user does not exist
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user details using the repository function and return the updated user
    return user_repository.update_user(user_id, request_data, db)