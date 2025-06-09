from fastapi import APIRouter, Depends, status, Request
from app.schemas.post import PostCreate
from app.services.post_service import PostService
from app.utils.auth import get_current_user
from app.middleware.payload_size import payload_size_limiter
from typing import Any

post_router = APIRouter()

@post_router.post("/", status_code=status.HTTP_201_CREATED)
async def add_post(
    request: Request,
    post_in: PostCreate,
    user: dict = Depends(get_current_user),
    _: None = Depends(payload_size_limiter(1024 * 1024))
) -> dict[str, Any]:
    """
    Creates a new post for the authenticated user.
    Validates payload size (1MB), saves post in memory, returns postID.
    Returns error for invalid/missing token.
    """
    post = PostService.add_post(user_id=int(user["user_id"]), text=post_in.text)
    return {
        "status": "success",
        "data": {"id": post.get("post_id")},
        "errors": None
    }
