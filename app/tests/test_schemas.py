import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate
from app.schemas.post import PostCreate

def test_user_create_valid():
    user = UserCreate(email="a@b.com", password="password123")
    assert user.email == "a@b.com"

def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(email="not-an-email", password="password123")

def test_post_create_valid():
    post = PostCreate(text="Some text")
    assert post.text == "Some text"

def test_post_create_empty():
    with pytest.raises(ValidationError):
        PostCreate(text="")
