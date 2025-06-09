from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import datetime
try:
    from datetime import UTC
except ImportError:
    from datetime import timezone
    UTC = timezone.utc

Base = declarative_base()

class User(Base):
    """
    SQLAlchemy model for user entity.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True, doc="User's email address")
    password = Column(String(255), nullable=False, doc="Hashed user password")
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(UTC), nullable=False, doc="User creation timestamp")
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(UTC), onupdate=lambda: datetime.datetime.now(UTC), nullable=False, doc="User update timestamp")
