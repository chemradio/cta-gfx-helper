from passlib.hash import bcrypt


class PasswordVerificationFailed(Exception):
    def __init__(self):
        ...


def generate_password_hash(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(password: str, stored_hash) -> bool:
    if not bcrypt.verify(password, stored_hash):
        raise PasswordVerificationFailed()
