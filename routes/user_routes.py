from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import user_service
from dependencies import get_db, get_current_user

# Create an APIRouter instance for user-related endpoints
router = APIRouter(prefix="/users", tags=["Users"])

# Endpoint to update the details of the currently authenticated user
@router.put("/me")
def update_user(request: dict, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Call the user_service function to update user details
    # Pass the user_id from the current_user dependency, the request data, and the database session
    return user_service.update_user_details(current_user["user_id"], request, db)