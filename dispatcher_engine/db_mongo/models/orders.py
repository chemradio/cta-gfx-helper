from io import BytesIO

from bson import ObjectId
from pydantic import BaseModel, EmailStr
from pydantic import Field as PydanticField

from custom_types.orders import OrderRequestType, OrderSource, OrderStatus
from db_mongo.models.types.objectID import PyObjectId
from db_mongo.models.users import User


class Order(BaseModel):
    id: PyObjectId | None = PydanticField(default=None, alias="_id")
    user_id: PyObjectId | None = PydanticField(default=None, alias="user_id")

    telegram_id: int | None = None
    email: EmailStr | None = None

    created: str | None = None

    status: OrderStatus | None = None
    request_type: OrderRequestType | None = None

    error: bool | None = None
    error_type: str | None = None

    ordered_from: OrderSource | None = None
    order_start_timestamp: str | None = None
    order_creation_end_timestamp: str | None = None

    link: str | None = None
    background_screenshot: bool | None = None
    background_link: str | None = None

    # screenshots / static images
    screenshots_ready: bool | None = None

    # video description
    is_two_layer: bool | None = None
    background_file: BytesIO | None = None
    foreground_file: BytesIO | None = None

    video_gfx_file: BytesIO | None = None
    video_gfx_ready: bool | None = None
    audio_file: BytesIO | None = None
    audio_enabled: bool | None = None

    send_success: bool | None = None

    # quote
    quote_enabled: bool | None = False
    quote_text: str | None = None
    quote_author_text: str | None = None

    # readtime
    readtime_result: str | None = None
    readtime_speed: int | None = None
    readtime_text: str | None = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str, PyObjectId: str}

    readtime_speed: int | None = None
    readtime_text: str | None = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str, PyObjectId: str}
