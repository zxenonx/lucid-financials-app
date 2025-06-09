from pydantic import BaseModel, EmailStr, constr, Field

class UserCreate(BaseModel):
    """
    Schema for user signup request.
    """
    email: EmailStr = Field(..., description="User's email address")
    password: constr(min_length=8, max_length=128) = Field(..., description="User password (min 8 chars)")

class UserResponse(BaseModel):
    """
    Schema for user response data.
    """
    id: int
    email: EmailStr
    created_at: str
    updated_at: str
