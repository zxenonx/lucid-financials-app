"""
Service for post storage with DB and cache.
"""
import datetime
from typing import Any
from threading import Lock
from app.repositories.post_repository import PostRepository
from sqlalchemy.orm import Session

# Add cache: user_id -> (timestamp, posts)
cache_store: dict[int, tuple[datetime.datetime, list]] = {}
cache_lock = Lock()

class PostService:
    """
    Handles post creation and retrieval with DB and cache.
    """
    @staticmethod
    def add_post(db: Session, user_id: int, text: str) -> dict[str, Any]:
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
    def get_posts(db: Session, user_id: int, cache_minutes: int = 5) -> list[dict[str, Any]]:
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
