from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserLogin
from sqlalchemy.orm import Session
from ..utils.hashing import hash_password, verify_password
from ..utils.jwt import create_access_token
from typing import Tuple, Optional

class AuthService:
    """Provides authentication services for user signup and login."""

    @staticmethod
    def signup(db: Session, user_in: UserCreate) -> Tuple[Optional[str], Optional[dict], Optional[str]]:
        """Registers a new user and return authentication details.

        Args:
            db (Session): The database session used for user creation.
            user_in (UserCreate): The registration data (email and password).

        Returns:
            Tuple[Optional[str], Optional[dict], Optional[str]]: (JWT token, user data dict, error message)
        """
        if UserRepository.get_by_email(db, user_in.email):
            return None, None, "Email already registered"
        hashed_pw = hash_password(user_in.password)
        user = UserRepository.create(db, user_in, hashed_pw)
        token = create_access_token({"user_id": user.id, "email": user.email})
        user_data = {
            "id": user.id,
            "email": user.email,
            "created_at": str(user.created_at),
            "updated_at": str(user.updated_at)
        }
        return token, user_data, None

    @staticmethod
    def login(db: Session, user_in: UserLogin) -> Tuple[Optional[str], Optional[dict], Optional[str]]:
        """Authenticates a user and return authentication details.

        Verifies the user's email and password. If valid, returns a JWT token and user data.
        Returns an error if authentication fails.

        Args:
            db (Session): The database session used for user lookup.
            user_in (UserLogin): The login credentials (email and password).

        Returns:
            Tuple[Optional[str], Optional[dict], Optional[str]]: (JWT token, user data dict, error message)
        """
        user = UserRepository.get_by_email(db, user_in.email)
        if not user:
            return None, None, "Invalid email or password"
        if not verify_password(user_in.password, user.password):
            return None, None, "Invalid email or password"
        token = create_access_token({"user_id": user.id, "email": user.email})
        user_data = {
            "id": user.id,
            "email": user.email,
            "created_at": str(user.created_at),
            "updated_at": str(user.updated_at)
        }
        return token, user_data, None
