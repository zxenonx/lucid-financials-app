"""
Service for in-memory post storage.
"""
import uuid
from datetime import datetime
from typing import Any

# In-memory storage: user_id: list of posts
data_store: dict[int, list] = {}

class PostService:
    """
    Handles in-memory post creation and retrieval.
    """
    @staticmethod
    def add_post(user_id: int, text: str) -> dict[str, Any]:
        post_id = str(uuid.uuid4())
        post = {
            "post_id": post_id,
            "user_id": user_id,
            "text": text,
            "created_at": datetime.now().isoformat()
        }
        data_store.setdefault(user_id, []).append(post)
        return post
