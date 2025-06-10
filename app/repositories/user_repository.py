from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate
from typing import Optional

class UserRepository:
    """Provides database operations related to User entities."""

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Retrieves a user from the database by their email address.

        Args:
            db (Session): The database session used for querying.
            email (str): The email address to search for.

        Returns:
            Optional[User]: The User object if found, otherwise None.
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db: Session, user_in: UserCreate, hashed_password: str) -> User:
        """Creates and persist a new user in the database.

        Args:
            db (Session): The database session used for committing the new user.
            user_in (UserCreate): The user registration data (email and password).
            hashed_password (str): The securely hashed password for the user.

        Returns:
            User: The newly created User object.
        """
        user = User(
            email=user_in.email,
            password=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
