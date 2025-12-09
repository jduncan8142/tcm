"""
Configuration management for TCM application.

Uses pydantic-settings to load configuration from environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Application settings
    app_name: str = "Test Case Management"
    debug: bool = False
    host: str = "127.0.0.1"
    port: int = 8000

    # Database settings
    database_url: str = "postgresql+asyncpg://tcm:tcm@localhost:5432/tcm"
    database_echo: bool = False

    # Security settings
    secret_key: str = "change-me-in-production"

    # Authentication & Session settings
    session_secret: str = "change-me-in-production-use-a-different-secret"
    session_timeout: int = 3600  # Session timeout in seconds (default: 1 hour)
    log_failed_logins: bool = True  # Enable logging of failed login attempts

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore extra environment variables (e.g., Docker-specific vars)
    )


settings = Settings()
