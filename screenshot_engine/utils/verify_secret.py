import os
from fastapi import Body

SECRET_KEY = os.getenv("INTERCONTAINER_SECRET")


def verify_secret(secret_key: str = Body(...)):
    return secret_key == SECRET_KEY
