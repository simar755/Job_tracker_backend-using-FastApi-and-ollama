# services/auth_service.py
from sqlalchemy.orm import Session
from models.user_model import User
from utils.hashing import hash_password, verify_password
from utils.jwt_handler import create_access_token
from repository import user_repository

# Service function to register a new user
def register_user(db: Session, name: str, email: str, password: str, role: str):
    # Check if a user with the given email already exists
    if user_repository.get_user_by_email(db, email):
        # Return None if the email is already in use
        return None
    # Hash the user's password before storing it
    hashed_pw = hash_password(password)
    # Create a new User model instance with the provided details
    new_user = User(name=name, email=email, password=hashed_pw, role=role)
    # Use the repository function to create the user in the database and return the created user
    return user_repository.create_user(db, new_user)

# Service function to log in a user
def login_user(db: Session, email: str, password: str):
    # Retrieve the user by email using the repository function
    user = user_repository.get_user_by_email(db, email)
    # Check if the user exists and the provided password matches the stored hash
    if user and verify_password(password, user.password):
        # Create an access token with user details (email, role, and ID)
        token = create_access_token(data={"sub": user.email, "role": user.role, "user_id": user.id})
        # Return the access token in a dictionary
        return {"access_token": token}
    # Return None if login fails (user not found or incorrect password)
    return None