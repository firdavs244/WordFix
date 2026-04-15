"""
Password hashing compatible with Django's PBKDF2 hasher.

Django stores passwords as: pbkdf2_sha256$<iterations>$<salt>$<base64hash>
This module can verify and create passwords in this exact format.
"""

import base64
import hashlib
import hmac
import os

# Django 5.x default iterations (2024+)
DJANGO_PBKDF2_ITERATIONS = 870000


def make_password(raw_password: str, iterations: int = DJANGO_PBKDF2_ITERATIONS) -> str:
    """
    Hash a password in Django PBKDF2 format.

    Returns: "pbkdf2_sha256$<iterations>$<salt>$<hash>"
    """
    salt = base64.b64encode(os.urandom(12)).decode("ascii")
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        raw_password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations,
    )
    hash_b64 = base64.b64encode(dk).decode("ascii")
    return f"pbkdf2_sha256${iterations}${salt}${hash_b64}"


def check_password(raw_password: str, encoded: str) -> bool:
    """
    Verify a raw password against a Django PBKDF2 hash.

    Args:
        raw_password: The plaintext password to verify.
        encoded: The stored hash in format "pbkdf2_sha256$<iter>$<salt>$<hash>"
    """
    try:
        algorithm, iterations_str, salt, stored_hash = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False

        iterations = int(iterations_str)
        dk = hashlib.pbkdf2_hmac(
            "sha256",
            raw_password.encode("utf-8"),
            salt.encode("utf-8"),
            iterations,
        )
        computed_hash = base64.b64encode(dk).decode("ascii")

        # Constant-time comparison
        return hmac.compare_digest(computed_hash, stored_hash)
    except (ValueError, TypeError):
        return False
