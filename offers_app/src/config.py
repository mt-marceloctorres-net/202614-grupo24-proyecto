from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación, leída de variables de entorno.

    Los valores por defecto sirven para correr en local; en Kubernetes cada campo
    llega por variable de entorno (`DB_HOST`, `DB_NAME`, …). pydantic-settings
    hace la correspondencia sin distinguir mayúsculas.

    Se usa `BaseSettings` en vez del patrón `@classmethod @property @lru_cache`
    de `pets_app`: esa combinación de decoradores quedó deprecada en Python 3.11
    y **fue eliminada en 3.13**, así que funciona hoy pero se rompe sola al
    actualizar el intérprete.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Offers app"
    log_level: str = "DEBUG"
    db_host: str = "localhost"
    db_port: str = "5432"
    db_name: str = "offers_db"
    db_user: str = "postgres"
    db_password: str = "postgres"

    @property
    def db_url(self) -> str:
        """Cadena de conexión de SQLAlchemy hacia Postgres."""
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
