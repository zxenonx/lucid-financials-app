"""
Application Settings Configuration.

This module handles all application configuration using environment variables
with proper validation and type checking using Pydantic settings.
"""
import os
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Application settings.
    """

    # Database Configuration - Updated for Aiven Cloud
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

    DATABASE_URL: str = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl-mode=REQUIRED&ssl-verify-cert=false&charset=utf8mb4"
    )

    print("Database URL:", DATABASE_URL)

    # Security Configuration
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        min_length=32,
        description="Secret key for JWT token encryption"
    )
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        ge=1,
        le=1440,
        description="JWT token expiration time in minutes"
    )
    BCRYPT_ROUNDS: int = Field(
        default=12,
        ge=10,
        le=15,
        description="Bcrypt hashing rounds for password security"
    )

    # Application Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(
        default=8000,
        ge=1000,
        le=65535,
        description="Server port"
    )
    DEBUG: bool = Field(default=False, description="Debug mode")

    # Cache Configuration
    CACHE_EXPIRE_MINUTES: int = Field(
        default=5,
        ge=1,
        le=60,
        description="Cache expiration time in minutes"
    )

    # Payload Configuration
    MAX_PAYLOAD_SIZE_MB: int = Field(
        default=1024 * 1024 ,
        description="Maximum payload size in megabytes"
    )

    class Config:
        """Pydantic configuration for settings."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

try:
    settings = Settings()
except Exception as e:
    print(f"Error loading settings: {e}")
    raise


def get_settings() -> Settings:
    """
    Dependency function to get application settings.

    Returns:
        Settings: The application settings instance
    """
    return settings

__all__ = ["settings", "get_settings", "Settings"]
