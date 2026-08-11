import hashlib
import hmac
import secrets


def hash_password(password: str) -> tuple[str, str]:
    """Genera el hash de una contraseña con un salt aleatorio.

    Returns:
        Una tupla (password_hash, salt), ambos en hexadecimal.
    """
    salt = secrets.token_hex(16)
    password_hash = _pbkdf2(password, salt)
    return password_hash, salt


def verify_password(password: str, password_hash: str, salt: str) -> bool:
    """Verifica que `password` corresponda al hash y salt almacenados."""
    return hmac.compare_digest(_pbkdf2(password, salt), password_hash)


def _pbkdf2(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000
    ).hex()
