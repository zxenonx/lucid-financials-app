from sqlalchemy.orm import Session
from app.models.post import Post
import uuid
from datetime import datetime

class PostRepository:
    @staticmethod
    def create(db: Session, user_id: int, text: str) -> Post:
        """Creates and persists a new post for a user.

        This method generates a new UUID for the post, sets the user ID, post content,
        and current timestamp, then saves the post to the database.

        Args:
            db (Session): The database session used for committing the new post.
            user_id (int): The unique identifier of the user creating the post.
            text (str): The content of the post.

        Returns:
            Post: The newly created Post object, refreshed from the database.
        """
        post = Post(
            id=str(uuid.uuid4()),
            user_id=user_id,
            text=text,
            created_at=datetime.now()
        )
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def get_by_user(db: Session, user_id: int) -> list[Post]:
        """Retrieves all posts for a given user, ordered by creation time DESC.

        This method queries the db for all posts associated with the specified user ID.
        The results are ordered from newest to oldest based on the post creation timestamp.

        Args:
            db (Session): The database session used for querying.
            user_id (int): The unique identifier of the user whose posts are to be retrieved.

        Returns:
            list[Post]: A list of Post objects belonging to the user, ordered by created_at DESC.
        """
        return db.query(Post).filter(Post.user_id == user_id).order_by(Post.created_at.desc()).all()
