"""Database Configuration and Setup.

This module handles SQLAlchemy database engine, session management,
and provides the base class for all database models.
"""

from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import logging
from typing import Generator

from .settings import settings

# Configure logging for database operations
logger = logging.getLogger(__name__)

# SQLAlchemy database engine
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_pre_ping=True,
    pool_recycle=1800,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    future=True,
    connect_args={
        "ssl_disabled": False,  # Enable SSL for Aiven
        "ssl_verify_identity": False,
        "autocommit": False,
        "charset": "utf8mb4",
        "sql_mode": "TRADITIONAL",
    },
    execution_options={
        "schema_translate_map": None,
        "compiled_cache": {}
    }
)

# Configure SQLAlchemy metadata with naming convention for constraints
metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

Base = declarative_base(metadata=metadata)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

def get_db() -> Generator[Session, None, None]:
    """
    Database dependency for FastAPI route handlers.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        logger.debug("Database session created")
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        logger.debug("Database session closed")
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for database sessions.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        logger.debug("Database context session created")
        yield db
        db.commit()
    except Exception as e:
        logger.error(f"Database context error: {e}")
        db.rollback()
        raise
    finally:
        logger.debug("Database context session closed")
        db.close()

def init_database():
    """
    Initialize the database by creating all tables.

    Raises:
        Exception: If database initialization fails
    """
    try:
        logger.info("Initializing database...")

        Base.metadata.create_all(bind=engine)

        try:
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            logger.info(f"Database initialized successfully. Tables created: {tables}")
        except Exception as inspect_error:
            logger.warning(f"Could not inspect tables after creation: {inspect_error}")
            logger.info("Database initialized successfully (table inspection failed)")

    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def drop_database():
    """
    Drop all database tables.

    Raises:
        Exception: If database drop operation fails
    """
    try:
        logger.warning("Dropping all database tables...")

        Base.metadata.drop_all(bind=engine)
        logger.warning("All database tables dropped")
    except Exception as e:
        logger.error(f"Failed to drop database tables: {e}")
        raise
