"""Password hashing and verification utilities."""

from passlib.context import CryptContext

# Initialize password hashing context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashes a plain text password using bcrypt.

    Args:
        password: The plain text password to be hashed.

    Returns:
        str: A securely hashed version of the password that can be safely stored.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a stored hash.

    Uses constant-time comparison to prevent timing attacks.

    Args:
        plain_password: The plain text password to verify.
        hashed_password: The hashed password to verify against.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
