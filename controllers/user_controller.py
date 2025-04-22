from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_current_user
from database import get_db
from models.user_model import User
from services import user_service

# Create an APIRouter instance for user-related endpoints
router = APIRouter(prefix="/users", tags=["Users"])

# Endpoint to update the name of the currently authenticated user
@router.put("/me")
def update_user(name: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Query the database for the user with the ID from the current_user dependency
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    # Update the user's name with the provided name
    user.name = name
    # Commit the changes to the database
    db.commit()
    # Return a success message
    return {"msg": "Details updated"}

# Function to update user information using the user service
def update_user_info(user_id: int, request: dict, db: Session):
    # Call the user_service function to update the user details
    # Pass the user ID, request data, and database session
    return user_service.update_user_details(user_id, request, db)