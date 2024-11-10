from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr
from pydantic import Field as PydanticField

from custom_types_enums.users import NormalUserPermission, UserRole
from db_mongo.models.types.objectID import PyObjectId


class User(BaseModel):
    id: PyObjectId = PydanticField(default=None, alias="_id")

    first_name: str | None = None
    username: str | None = None
    telegram_id: int | None = None
    email: EmailStr | None = None

    created: str | None = None
    password_hash: str | None = None
    role: UserRole | None = None
    permission: NormalUserPermission | None = None

    description: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    orders: list | None = None
    read_speed_wpm: int | None = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str, PyObjectId: str}
