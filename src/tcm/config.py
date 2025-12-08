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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
