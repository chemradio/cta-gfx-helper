from datetime import datetime

import jwt

from config import JWT_SECRET


def generate_jwt_token(data: dict) -> str:
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    return jwt.encode(data, JWT_SECRET)


def decode_jwt_payload(payload: str) -> dict:
    if "Bearer " in payload:
        payload = payload[7:]
    return jwt.decode(payload, JWT_SECRET, algorithms=["HS256"])
