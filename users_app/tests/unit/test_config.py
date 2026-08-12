from config import Settings


def test_settings_have_defaults():
    """Los settings tienen valores por defecto razonables cuando no hay variables de ambiente."""
    assert Settings.app_name
    assert Settings.log_level
    assert Settings.db_host
    assert Settings.db_port
    assert Settings.db_name
    assert Settings.db_user
    assert Settings.db_password
    assert "postgresql://" in Settings.db_url
    assert Settings.token_expiration_minutes > 0
