import os
from functools import lru_cache


class Settings:
    """Application settings."""

    @staticmethod
    @lru_cache()
    def database_url() -> str:
        """Build the database URL from environment variables."""
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "routes_db")
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "postgres")
        return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    @staticmethod
    @lru_cache()
    def app_name() -> str:
        return os.getenv("APP_NAME", "Routes app")

    @staticmethod
    @lru_cache()
    def log_level() -> str:
        return os.getenv("LOG_LEVEL", "INFO")
