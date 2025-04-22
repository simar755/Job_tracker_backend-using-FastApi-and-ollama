from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from utils.hashing import hash_password, verify_password
from utils.jwt_handler import create_access_token
from models.user_model import User

# Create an APIRouter instance for authentication-related endpoints
router = APIRouter(prefix="/auth", tags=["Auth"])

# Endpoint to register a new user
@router.post("/register")
def register(name: str, email: str, password: str, role: str, db: Session = Depends(get_db)):
    # Check if a user with the given email already exists in the database
    if db.query(User).filter(User.email == email).first():
        # Raise an HTTPException with a 400 Bad Request status if the email is already registered
        raise HTTPException(status_code=400, detail="Email already registered")
    # Create a new User object with the provided details, hashing the password
    user = User(name=name, email=email, password=hash_password(password), role=role)
    # Add the user object to the database session
    db.add(user)
    # Commit the changes to the database
    db.commit()
    # Return a success message
    return {"message": "Registered successfully"}

# Endpoint to log in a user
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    # Query the database for the user with the given email
    user = db.query(User).filter(User.email == email).first()
    # Check if the user exists and the provided password matches the stored hash
    if not user or not verify_password(password, user.password):
        # Raise an HTTPException with a 401 Unauthorized status if the credentials are invalid
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Create an access token with user details (email, role, and ID)
    token = create_access_token({"sub": user.email, "role": user.role, "user_id": user.id})
    # Return the access token and token type
    return {"access_token": token, "token_type": "bearer"}