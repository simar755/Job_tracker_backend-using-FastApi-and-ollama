import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the secret key for JWT encoding/decoding from the environment variables
SECRET_KEY = os.getenv("SECRET_KEY")

# Retrieve the algorithm used for JWT encoding from the environment variables
ALGORITHM = os.getenv("ALGORITHM")

# Retrieve the access token expiration time (in minutes) from the environment variables, defaulting to 30 minutes if not set
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Retrieve the database URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")