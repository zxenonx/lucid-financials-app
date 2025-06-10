from fastapi import APIRouter, Depends, status, Request
from app.schemas.post import PostCreate
from app.services.post_service import PostService
from app.utils.auth import get_current_user
from app.middleware.payload_size import payload_size_limiter
from app.config.database import get_db
from typing import Any

post_router = APIRouter()

@post_router.post("/", status_code=status.HTTP_201_CREATED)
async def add_post(
    request: Request,
    post_in: PostCreate,
    user: dict = Depends(get_current_user),
    db = Depends(get_db),
    _: None = Depends(payload_size_limiter(1024 * 1024))
) -> dict[str, Any]:
    """Creates a new post for the authenticated user.

    This endpoint allows an authenticated user to create a new post.
    The request payload must contain the post content, and the payload size is limited to 1MB.
    The function performs the following steps:

    - Validates the user's authentication token and retrieves the user from the request context.
    - Validates the payload size to ensure it does not exceed the maximum allowed size (1MB).
    - Persists the new post to the database, associating it with the authenticated user's ID.
    - Returns a JSON response containing the new post's unique identifier upon success.
    - Returns an error response if the authentication token is missing or invalid, or if any validation fails.

    Args:
        request (Request): The incoming HTTP request object.
        post_in (PostCreate): The Pydantic model containing the post data from the request body.
        user (dict): The authenticated user's information, injected by the dependency.
        db: The database session, injected by the dependency.
        _ (None): Used to enforce the payload size limit via dependency injection.

    Returns:
        dict[str, Any]: A dictionary with the status, the new post's ID on success, and error details if applicable.

    Raises:
        HTTPException: If authentication fails or payload is invalid.
    """
    post = PostService.add_post(db, user_id=int(user["user_id"]), text=post_in.text)
    return {
        "status": "success",
        "data": {"id": post.get("post_id")},
        "errors": None
    }

@post_router.get("/", status_code=status.HTTP_200_OK)
async def get_posts(
    user: dict = Depends(get_current_user),
    db = Depends(get_db)
) -> dict[str, Any]:
    """Retrieves all posts for the authenticated user.

    This endpoint allows an authenticated user to fetch all their posts.
    The response is cached for 5 minutes per user to improve performance and reduce database load.
    The function performs the following steps:

    - Validates the user's authentication token and retrieves the user from the request context.
    - Fetches all posts associated with the authenticated user's ID from the database.
    - Returns a JSON response containing the list of posts on success.
    - Returns an error response if the authentication token is missing or invalid.

    Args:
        user (dict): The authenticated user's information, injected by the dependency.
        db: The database session, injected by the dependency.

    Returns:
        dict[str, Any]: A dictionary with the status, a list of the user's posts on success, and error details if applicable.

    Raises:
        HTTPException: If authentication fails.
    """
    posts = PostService.get_posts(db, user_id=int(user["user_id"]))
    return {
        "status": "success",
        "data": posts,
        "errors": None
    }
