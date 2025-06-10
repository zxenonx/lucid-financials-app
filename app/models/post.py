import uuid

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from app.config.database import Base
import datetime
try:
    from datetime import UTC
except ImportError:
    from datetime import timezone
    UTC = timezone.utc

class Post(Base):
    """
    SQLAlchemy model for post entity.
    """
    __tablename__ = "posts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True, doc="Post UUID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, doc="User ID")
    text = Column(Text, nullable=False, doc="Post text, max 1MB")
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(UTC), nullable=False, doc="Post creation timestamp")
