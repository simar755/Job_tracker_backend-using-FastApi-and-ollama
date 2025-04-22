# repository/user_repository.py
from sqlalchemy.orm import Session
from models.user_model import User

# Repository function to retrieve a user by email
def get_user_by_email(db: Session, email: str):
    # Query the database for a user with the given email and return the first matching result
    return db.query(User).filter(User.email == email).first()

# Repository function to create a new user
def create_user(db: Session, user: User):
    # Add the user object to the database session
    db.add(user)
    # Commit the changes to the database
    db.commit()
    # Refresh the user object to get the updated state from the database
    db.refresh(user)
    # Return the created user object
    return user

# Repository function to retrieve a user by their ID
def get_user_by_id(user_id: int, db: Session):
    # Query the database for a user with the given ID and return the first matching result
    return db.query(User).filter(User.id == user_id).first()

# Repository function to update an existing user's details
def update_user(user_id: int, request_data: dict, db: Session):
    # Query the database for the user with the given ID
    user = db.query(User).filter(User.id == user_id).first()

    # Update the user's attributes if they are present in the request data
    if "name" in request_data:
        user.name = request_data["name"]
    if "email" in request_data:
        user.email = request_data["email"]
    if "password" in request_data:
        user.password = request_data["password"]
    if "role" in request_data:
        user.role = request_data["role"]

    # Commit the changes to the database
    db.commit()
    # Refresh the user object to get the updated state from the database
    db.refresh(user)
    # Return a dictionary containing a success message and the updated user details
    return {"message": "User updated successfully", "user": {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }}