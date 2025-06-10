"""JSON Web Token (JWT) utility functions.

This module provides functionality for creating JWT access tokens used for
authentication and authorization in the application. It uses the python-jose
library for JWT operations and handles token expiration.
"""

from jose import jwt
from datetime import datetime, timedelta
try:
    from datetime import UTC  
except ImportError:
    from datetime import timezone
    UTC = timezone.utc

from app.config.settings import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """Creates a new JWT access token with the provided data.

    The token will include an expiration time and can be used for authenticating
    subsequent requests. The token is signed using the application's secret key.

    Args:
        data: Dictionary containing the claims to include in the token.
        expires_delta: int. Token expiration time in minutes.

    Returns:
        str: A JWT token string that can be used for authentication.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
