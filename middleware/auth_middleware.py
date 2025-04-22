from fastapi import Request, HTTPException, status
from utils.jwt_handler import verify_token

async def auth_middleware(request: Request, call_next):
    """
    Middleware to authenticate requests using JWT tokens from the Authorization header.

    Args:
        request (Request): The incoming request object.
        call_next (Callable): The next middleware or route handler in the chain.

    Returns:
        Response: The response from the next middleware or route handler.

    Raises:
        HTTPException: If the Authorization header is missing or the token is invalid.
    """
    # Retrieve the Authorization header from the request headers
    token = request.headers.get("Authorization")

    # Check if the Authorization header is missing
    if not token:
        # Raise an HTTPException with a 401 Unauthorized status if the header is missing
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")

    try:
        # Verify the JWT token by splitting the Bearer token and passing the token part.
        # It expects the token to be in the format "Bearer <token>"
        verify_token(token.split(" ")[1])
    except Exception as e:
        # Raise an HTTPException with a 401 Unauthorized status if the token is invalid
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # If the token is valid, call the next middleware or route handler in the chain
    return await call_next(request)