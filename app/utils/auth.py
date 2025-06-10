from fastapi import HTTPException, status, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from app.config.settings import settings
from typing import Dict, Any

bearer_scheme = HTTPBearer()

def get_current_user(request: Request,
                     credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
                     ) -> Dict[str, Any]:
    """Extracts and validates the JWT from the Authorization header.

    This dependency retrieves the JWT from the request's Authorization header, decodes and verifies it,
    and returns the user's information if the token is valid.
    If the token is missing, invalid, or expired, it raises an HTTPException with 401 Unauthorized.

    Args:
        request (Request): The incoming HTTP request object.
        credentials (HTTPAuthorizationCredentials): The bearer token credentials extracted from the header.

    Returns:
        Dict[str, Any]: A dictionary containing the user's ID and email if authentication is successful.

    Raises:
        HTTPException: If the token is missing, invalid, expired, or the payload is malformed.
    """
    token = credentials.credentials if credentials else None
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        email = payload.get("email")
        if user_id is None or email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return {"user_id": user_id, "email": email}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
