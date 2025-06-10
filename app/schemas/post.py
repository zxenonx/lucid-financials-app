from pydantic import BaseModel, constr, Field

class PostCreate(BaseModel):
    """Schema for creating a post."""
    text: constr(min_length=1) = Field(..., description="Post text (max 1MB)")

class PostResponse(BaseModel):
    """Schema for returning a post."""
    post_id: str
    text: str
    user_id: int
    created_at: str
