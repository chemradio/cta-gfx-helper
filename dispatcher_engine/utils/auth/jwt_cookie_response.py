from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from db_tortoise.users_models import User, User_Pydantic
from utils.auth.token_manupulation import generate_jwt_token


async def generate_cookie_json_response(user: User) -> JSONResponse:
    # convert tortoise model to pydantic and convert unserializable fields
    user_py = await User_Pydantic.from_tortoise_orm(user)
    user_py_jsonable = jsonable_encoder(user_py)

    # add a cookie with a jwt-token to the response
    access_token = generate_jwt_token(user_py_jsonable)
    response = JSONResponse(content=user_py_jsonable)
    response.set_cookie(key="jwt", value=f"Bearer {access_token}")
    return response
