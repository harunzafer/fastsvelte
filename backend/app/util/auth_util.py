from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Match Node's settings
ph = PasswordHasher(
    time_cost=2,  # Iterations
    memory_cost=19456,  # In KiB => 19 MB
    parallelism=1,
    hash_len=32,
)


def hash_password(password: str) -> str:
    """Hash password using Argon2id (like @node-rs/argon2)."""
    return ph.hash(password)


def verify_password_hash(stored_hash: str, password: str) -> bool:
    """Verify password against stored Argon2 hash."""
    try:
        return ph.verify(stored_hash, password)
    except VerifyMismatchError:
        return False
