"""
Service for post storage with DB and cache.
"""
import datetime
from typing import Any
from threading import Lock
from app.repositories.post_repository import PostRepository
from sqlalchemy.orm import Session
from app.config.settings import settings

# Add cache: user_id -> (timestamp, posts)
cache_store: dict[int, tuple[datetime.datetime, list]] = {}
cache_lock = Lock()

class PostService:
    """Provides methods to create, retrieve, and delete posts using the database and in-memory cache."""

    @staticmethod
    def add_post(db: Session, user_id: int, text: str) -> dict[str, Any]:
        """Creates a new post for a user, stores it in the database, and invalidates the user's cache.

        Args:
            db (Session): The database session used for creating the post.
            user_id (int): The ID of the user creating the post.
            text (str): The content of the post.

        Returns:
            dict[str, Any]: The created post data.
        """
        post_obj = PostRepository.create(db, user_id, text)
        post = {
            "post_id": post_obj.id,
            "user_id": post_obj.user_id,
            "text": post_obj.text,
            "created_at": post_obj.created_at.isoformat()
        }

        # Invalidate cache for this user
        with cache_lock:
            if user_id in cache_store:
                del cache_store[user_id]
        return post

    @staticmethod
    def get_posts(db: Session, user_id: int,
                  cache_minutes: int = settings.CACHE_EXPIRE_MINUTES) -> list[dict[str, Any]]:
        """Retrieves all posts for a user, using the cache if available and valid.

        Args:
            db (Session): The database session used for fetching posts.
            user_id (int): The ID of the user whose posts are being fetched.
            cache_minutes (int): The cache validity period in minutes (from env).

        Returns:
            list[dict[str, Any]]: A list of post data for the user.
        """
        now = datetime.datetime.now()
        with cache_lock:
            if user_id in cache_store:
                ts, posts = cache_store[user_id]
                if now - ts < datetime.timedelta(minutes=cache_minutes):
                    return posts

            # Cache miss or expired: fetch from DB
            post_objs = PostRepository.get_by_user(db, user_id)
            posts = [
                {
                    "post_id": p.id,
                    "user_id": p.user_id,
                    "text": p.text,
                    "created_at": p.created_at.isoformat()
                }
                for p in post_objs
            ]
            cache_store[user_id] = (now, posts)
            return posts

    @staticmethod
    def delete_post(db: Session, user_id: int, post_id: str) -> bool:
        """Deletes a post by ID for a user from both the database and the cache.

        Args:
            db (Session): The database session used for deletion.
            user_id (int): The ID of the user who owns the post.
            post_id (str): The ID of the post to delete.

        Returns:
            bool: True if the post was deleted, False otherwise.
        """
        deleted = PostRepository.delete(db, user_id, post_id)

        # Remove post from memory cache if present
        with cache_lock:
            if user_id in cache_store:
                ts, posts = cache_store[user_id]
                filtered_posts = [p for p in posts if p.get("post_id") != post_id]
                cache_store[user_id] = (ts, filtered_posts)
        return deleted
