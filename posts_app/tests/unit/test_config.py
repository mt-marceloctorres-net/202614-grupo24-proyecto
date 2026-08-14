from config import Settings


def test_settings_have_defaults():
    """Los settings tienen valores por defecto razonables cuando no hay variables de ambiente."""
    settings = Settings()
    assert settings.app_name
    assert settings.log_level
    assert settings.db_host
    assert settings.db_port
    assert settings.db_name
    assert settings.db_user
    assert settings.db_password
    assert "postgresql://" in settings.db_url


def test_db_url_reflects_env(monkeypatch):
    """`db_url` se arma con host/puerto/usuario/password/nombre configurados."""
    monkeypatch.setenv("DB_HOST", "posts-db-service")
    monkeypatch.setenv("DB_NAME", "posts_db")
    settings = Settings()
    assert settings.db_url == (
        "postgresql://postgres:postgres@posts-db-service:5432/posts_db"
    )
