from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status
from config import SECRET_KEY, ALGORITHM

# Function to create an access token using JWT
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)): #changed to 30 minutes.
    # Create a copy of the data to encode
    to_encode = data.copy()
    # Calculate the expiration time for the token
    expire = datetime.utcnow() + expires_delta
    # Update the data with the expiration time
    to_encode.update({"exp": expire})
    # Encode the data into a JWT and return it
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to verify a JWT token
def verify_token(token: str):
    try:
        # Decode the JWT token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Return the decoded payload if the token is valid
        return payload
    except JWTError:
        # Raise an HTTPException with a 401 Unauthorized status if the token is invalid
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")