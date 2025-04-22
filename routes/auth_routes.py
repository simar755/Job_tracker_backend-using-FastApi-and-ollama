# routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from services import auth_service
from dependencies import get_db
from pydantic import BaseModel, Field, EmailStr, validator
import re

# Define a Pydantic model for user registration data
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(..., examples=["user", "hr", "admin"])

    @validator("password")
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
        return value

# Define a Pydantic model for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

    @validator("password")
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
        return value

# Create an APIRouter instance for authentication-related endpoints
router = APIRouter(prefix="/auth", tags=["Auth"])

# Endpoint to register a new user
@router.post("/register")
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    result = auth_service.register_user(db, user.name, user.email, user.password, user.role)
    if not result:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message": "User registered successfully"}

# Endpoint to log in a user
@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    token = auth_service.login_user(db, user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token
