import pytest
from pydantic import ValidationError

from domain.models.user import User, UserStatus


def test_create_user_with_valid_data(valid_user_data):
    """Un usuario con datos válidos se crea correctamente."""
    user = User(**valid_user_data)

    assert user.id is None
    assert user.username == valid_user_data["username"]
    assert user.email == valid_user_data["email"]
    assert user.status == UserStatus.POR_VERIFICAR


def test_create_user_with_username_containing_spaces(valid_user_data):
    """El username no puede contener espacios."""
    with pytest.raises(ValidationError) as exc_info:
        User(**{**valid_user_data, "username": "j doe"})

    assert "username" in str(exc_info.value)


def test_create_user_with_username_containing_special_chars(valid_user_data):
    """El username no puede contener caracteres especiales."""
    with pytest.raises(ValidationError) as exc_info:
        User(**{**valid_user_data, "username": "jdoe!"})

    assert "username" in str(exc_info.value)


def test_create_user_with_empty_username(valid_user_data):
    """El username no puede estar vacío."""
    with pytest.raises(ValidationError):
        User(**{**valid_user_data, "username": ""})


def test_create_user_with_invalid_email(valid_user_data):
    """El email debe tener formato válido."""
    with pytest.raises(ValidationError) as exc_info:
        User(**{**valid_user_data, "email": "no-es-un-correo"})

    assert "email" in str(exc_info.value)


def test_create_user_without_password(valid_user_data):
    """La contraseña es obligatoria."""
    data = {k: v for k, v in valid_user_data.items() if k != "password"}
    with pytest.raises(ValidationError):
        User(**data)


def test_create_user_optional_fields_default_to_none():
    """Los campos opcionales no requieren valor."""
    user = User(username="minimal", password="pass", email="min@example.com")

    assert user.dni is None
    assert user.fullName is None
    assert user.phoneNumber is None
    assert user.status == UserStatus.POR_VERIFICAR
