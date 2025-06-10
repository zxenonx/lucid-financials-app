from unittest.mock import MagicMock
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserLogin

class DummyUser:
    def __init__(self, id=1, email="a@b.com", password="hashed", created_at="now", updated_at="now"):
        self.id = id
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at

def test_signup_email_already_registered(monkeypatch):
    db = MagicMock()
    user_in = UserCreate(email="a@b.com", password="pw90jfuwhiuw")
    monkeypatch.setattr("app.repositories.user_repository.UserRepository.get_by_email", lambda db, email: DummyUser())
    token, user_data, error = AuthService.signup(db, user_in)

    assert token is None and user_data is None and error == "Email already registered"

def test_signup_success(monkeypatch):
    db = MagicMock()
    user_in = UserCreate(email="b@b.com", password="pwasw99onwjw")
    monkeypatch.setattr("app.repositories.user_repository.UserRepository.get_by_email", lambda db, email: None)
    monkeypatch.setattr("app.services.auth_service.hash_password", lambda pw: "hashed")

    dummy_user = DummyUser(email="b@b.com")

    monkeypatch.setattr("app.repositories.user_repository.UserRepository.create",
                        lambda db, user_in, hashed_pw: dummy_user)
    monkeypatch.setattr("app.services.auth_service.create_access_token",
                        lambda payload: "token")
    token, user_data, error = AuthService.signup(db, user_in)

    assert token == "token"
    assert user_data["email"] == "b@b.com"
    assert error is None

def test_login_invalid_email(monkeypatch):
    db = MagicMock()
    user_in = UserLogin(email="notfound@b.com", password="pw09uhwuejbsjw")
    monkeypatch.setattr("app.repositories.user_repository.UserRepository.get_by_email", lambda db, email: None)
    token, user_data, error = AuthService.login(db, user_in)

    assert token is None and user_data is None and error == "Invalid email or password"

def test_login_invalid_password(monkeypatch):
    db = MagicMock()
    user_in = UserLogin(email="a@b.com", password="wrong00ybun8")
    user = DummyUser(password="hashed")

    monkeypatch.setattr("app.repositories.user_repository.UserRepository.get_by_email", lambda db, email: user)
    monkeypatch.setattr("app.services.auth_service.verify_password", lambda plain, hashed: False)
    token, user_data, error = AuthService.login(db, user_in)

    assert token is None and user_data is None and error == "Invalid email or password"

def test_login_success(monkeypatch):
    db = MagicMock()
    user_in = UserLogin(email="a@b.com", password="pw00bdswuruwiu")
    user = DummyUser(password="hashed")
    monkeypatch.setattr("app.repositories.user_repository.UserRepository.get_by_email", lambda db, email: user)
    monkeypatch.setattr("app.services.auth_service.verify_password", lambda plain, hashed: True)
    monkeypatch.setattr("app.services.auth_service.create_access_token", lambda payload: "token")
    token, user_data, error = AuthService.login(db, user_in)

    assert token == "token"
    assert user_data["email"] == "a@b.com"
    assert error is None
