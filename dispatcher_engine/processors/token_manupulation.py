import jwt

from config import JWT_SECRET


def generate_jwt_token(data: dict) -> str:
    return jwt.encode(data, JWT_SECRET)


def decode_jwt_payload(payload: str) -> dict:
    try:
        return jwt.decode(payload, JWT_SECRET, algorithms=["HS256"])
    except Exception as e:
        print(e)
        return False
