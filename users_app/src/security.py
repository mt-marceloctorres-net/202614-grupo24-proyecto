import hashlib
import secrets


def hash_password(password: str) -> tuple[str, str]:
    """Genera el hash de una contraseña con un salt aleatorio.

    Returns:
        Una tupla (password_hash, salt), ambos en hexadecimal.
    """
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000
    ).hex()
    return password_hash, salt
