from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación, leída de variables de ambiente.

    Usa `pydantic-settings` en vez del patrón `@classmethod + @property +
    @lru_cache()` (deprecado en Python 3.11 y eliminado en 3.13): cada campo
    se resuelve desde el ambiente en el momento de instanciar `Settings`.
    """

    model_config = SettingsConfigDict(case_sensitive=False)

    app_name: str = "Posts app"
    log_level: str = "DEBUG"
    db_host: str = "localhost"
    db_port: str = "5432"
    db_name: str = "posts_db"
    db_user: str = "postgres"
    db_password: str = "postgres"

    @property
    def db_url(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
