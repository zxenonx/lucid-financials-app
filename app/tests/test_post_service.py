from unittest.mock import patch, MagicMock
from app.services.post_service import PostService
from datetime import datetime

class DummyPost:
    def __init__(self, id, user_id, text, created_at):
        self.id = id
        self.user_id = user_id
        self.text = text
        self.created_at = created_at

class DummyDB:
    def __init__(self):
        self.query = MagicMock()


def test_add_post_invalidates_cache(monkeypatch):
    db = DummyDB()
    user_id = 1
    text = "Test post"
    post_obj = DummyPost("pid", user_id, text, MagicMock(isoformat=lambda: "now"))
    monkeypatch.setattr("app.services.post_service.PostRepository.create", lambda db, uid, txt: post_obj)

    cache_dict = {user_id: (None, ["old post"])}
    monkeypatch.setattr("app.services.post_service.cache_store", cache_dict)
    PostService.cache_store = cache_dict  # Same object, not a new dict

    post = PostService.add_post(db, user_id, text)
    assert post["user_id"] == user_id
    assert user_id not in PostService.cache_store


def test_get_posts_cache_and_db(monkeypatch):
    db = DummyDB()
    user_id = 2

    # Test cache hit
    now = datetime(2025, 6, 10, 14, 56, 25)
    monkeypatch.setattr("app.services.post_service.cache_store",
                        {user_id: (
                        now, [{"post_id": "1", "user_id": user_id, "text": "cached", "created_at": "now"}])})

    with patch("app.services.post_service.datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = now
        posts = PostService.get_posts(db, user_id)
        assert posts[0]["text"] == "cached"

    # Test cache miss
    monkeypatch.setattr("app.services.post_service.cache_store", {})
    dummy_post = DummyPost("2", user_id, "from db", MagicMock(isoformat=lambda: "now"))
    monkeypatch.setattr("app.services.post_service.PostRepository.get_by_user", lambda db, uid: [dummy_post])
    with patch("app.services.post_service.datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = now
        posts = PostService.get_posts(db, user_id, cache_minutes=0)

        assert posts, "Returned posts is empty!"
        assert posts[0]["text"] == "from db"

def test_delete_post_removes_from_cache(monkeypatch):
    db = DummyDB()
    user_id = 3
    post_id = "pid"
    cache_dict = {user_id: (MagicMock(), [{"post_id": post_id}, {"post_id": "other"}])}

    monkeypatch.setattr("app.services.post_service.cache_store", cache_dict)
    PostService.cache_store = cache_dict
    monkeypatch.setattr("app.services.post_service.PostRepository.delete", lambda db, uid, pid: True)

    deleted = PostService.delete_post(db, user_id, post_id)
    assert deleted is True

    # Check that the post was removed from cache
    assert all(p["post_id"] != post_id for p in PostService.cache_store[user_id][1])
