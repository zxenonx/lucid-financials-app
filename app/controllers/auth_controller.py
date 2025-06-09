"""
Authentication controller: defines signup and login endpoints.
"""
from typing import Any

from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate, UserLogin
from ..services.auth_service import AuthService
from ..config.database import get_db
from fastapi.responses import JSONResponse

auth_router = APIRouter()

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(request: Request, user_in: UserCreate, db: Session = Depends(get_db)) -> dict[str, Any]:
    """
    Signup endpoint for registering a new user.

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
            "token": token,
            "user": user_data
        },
        "errors": None
    }

@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: Request, user_in: UserLogin, db: Session = Depends(get_db)) -> dict[str, Any]:
    """
    Login endpoint for authenticating a user.
    Accepts email and password, returns JWT token if valid.
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
            "token": token,
            "user": user_data
        },
        "errors": None
    }
