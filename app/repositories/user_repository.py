from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate
from typing import Optional

class UserRepository:
    """
    Repository for user DB operations.
    """
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Fetch user by email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db: Session, user_in: UserCreate, hashed_password: str) -> User:
        """Create a new user."""
        user = User(
            email=user_in.email,
            password=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
