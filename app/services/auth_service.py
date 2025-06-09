from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate
from sqlalchemy.orm import Session
from ..utils.hashing import hash_password
from ..utils.jwt import create_access_token
from typing import Tuple, Optional

class AuthService:
    """
    Handles user signup logic: validation, hashing, token generation.
    """
    @staticmethod
    def signup(db: Session, user_in: UserCreate) -> Tuple[Optional[str], Optional[dict], Optional[str]]:
        """
        Signup a new user, return (token, user_data, error).
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
