# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL  # Import DATABASE_URL from config.py

# Create a SQLAlchemy engine to connect to the database
# connect_args={"check_same_thread": False} is used for SQLite in development, remove in production
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a SessionLocal class to manage database sessions
SessionLocal = sessionmaker(bind=engine, autoflush=False)

# Create a declarative base class for defining SQLAlchemy models
Base = declarative_base()

# Function to get a database session
def get_db():
    # Create a new database session
    db = SessionLocal()
    try:
        # Yield the database session to the request
        yield db
    finally:
        # Close the database session after the request is finished
        db.close()