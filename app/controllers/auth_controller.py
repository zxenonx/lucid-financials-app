from typing import Any

from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate, UserLogin
from ..services.auth_service import AuthService
from ..config.database import get_db

auth_router = APIRouter()

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(request: Request, user_in: UserCreate, db: Session = Depends(get_db)) -> dict[str, Any]:
    """Registers a new user.

    Args:
        request (Request): Request object
        user_in (UserCreate): User signup data (email, password)
        db (Session): Database session

    Returns:
        dict: API response with token or error
    """
    token, user_data, error = AuthService.signup(db, user_in)
    if error:
        return {
            "status": "error",
            "data": None,
            "errors": [error]
        }
    return {
        "status": "success",
        "data": {
            "token": token        },
        "errors": None
    }

@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: Request, user_in: UserLogin, db: Session = Depends(get_db)) -> dict[str, Any]:
    """Authenticates a user and return a JWT access token.

    This endpoint verifies the user's email and password credentials.
    If authentication is successful, it returns a JWT token and user details.
    Otherwise, it returns an error message.

    Args:
        request (Request): The incoming HTTP request object.
        user_in (UserLogin): The login credentials (email and password) provided by the user.
        db (Session): The database session dependency.

    Returns:
        dict[str, Any]: A dictionary containing the authentication status, JWT token and user info
        on success, or error details on failure.
    """
    token, user_data, error = AuthService.login(db, user_in)
    if error:
        return {
            "status": "error",
            "data": None,
            "errors": [error]
        }
    return {
        "status": "success",
        "data": {
            "token": token
        },
        "errors": None
    }
