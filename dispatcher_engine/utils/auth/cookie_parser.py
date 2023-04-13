from fastapi import Cookie

from db_tortoise.users_models import User, User_Pydantic
from utils.auth.token_manupulation import decode_jwt_payload


async def cookie_parser(jwt: str | None = Cookie(None)):
    try:
        print("cookie parser started")
        print("jwt: ", jwt)
        user_dict = decode_jwt_payload(jwt)
        print(user_dict)
        # check user exists
        user_db = await User.filter(email=user_dict.get("email"))
        if not user_db:
            return None
        # check user consistency
        ...

        # check user role
        ...

        return User_Pydantic(**user_dict)
    except:
        return None
