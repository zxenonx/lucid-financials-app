from app.utils.hashing import hash_password, verify_password

def test_hash_and_verify_password():
    pw = "super-secret"
    hashed = hash_password(pw)
    assert verify_password(pw, hashed)
    assert not verify_password("wrong", hashed)
