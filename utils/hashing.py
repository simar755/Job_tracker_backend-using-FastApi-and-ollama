from passlib.context import CryptContext

# Initialize a CryptContext for password hashing and verification using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password using bcrypt
def hash_password(password: str):
    # Hash the provided password and return the hashed value
    return pwd_context.hash(password)

# Function to verify a plain password against a hashed password
def verify_password(plain_password: str, hashed_password: str):
    # Verify if the plain password matches the hashed password
    return pwd_context.verify(plain_password, hashed_password)