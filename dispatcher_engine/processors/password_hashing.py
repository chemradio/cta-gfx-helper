from passlib.hash import bcrypt


class PasswordVerificationFailed(Exception):
    def __init__(self):
        ...


def generate_password_hash(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(password: str, stored_hash) -> bool:
    if not bcrypt.verify(password, stored_hash):
        raise PasswordVerificationFailed()


x = generate_password_hash("123")
y = verify_password("1234", x)

print(y)
