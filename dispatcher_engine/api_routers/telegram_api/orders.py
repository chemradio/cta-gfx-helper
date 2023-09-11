from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Form,
    HTTPException,
    Request,
    UploadFile,
)
from pydantic import BaseModel, HttpUrl

from container_interaction.signal_sender import signal_to_services
from db_tortoise.order_controller import OrderController
from db_tortoise.orders_models import Order, Order_Pydantic, OrderIn_Pydantic
from db_tortoise.users_models import User, User_Pydantic
from utils.auth.cookie_parser import cookie_parser

router = APIRouter()


class TelegramOrderIn(BaseModel):
    request_type: str
    telegram_id: int
    order_creation_end_timestamp: int
    order_start_timestamp: int

    status: str | None = None
    stage: str | None = None

    quote_enabled: bool | None = False
    quote_text: str | None = None
    quote_author_text: str | None = None
    quote_author_enabled: bool | None = None

    audio_enabled: bool | None = False
    audio_name: str | None = None

    foreground_name: str | None = None
    background_name: str | None = None
    bg_animation: str | None = None
    fg_animation: str | None = None

    background_screenshot: bool = False
    background_link: str | None = None

    is_two_layer: bool | None = False

    link: str | None = None
    ordered_from: str = "telegram"


@router.post("/")
async def add_order(
    background_tasks: BackgroundTasks, order_in: TelegramOrderIn, request: Request
):
    order_dict = order_in.dict()
    print(f"{order_dict=}")
    user_telegram_id = order_dict.pop("telegram_id")

    user = await User.filter(telegram_id=user_telegram_id).first()

    order_db = await Order(**order_in.dict(), user=user)

    order_db.quote_author_enabled = True if order_in.quote_author_text else False

    await OrderController.advance_order_stage(order_db)
    await order_db.save()
    await order_db.refresh_from_db()

    background_tasks.add_task(signal_to_services, order_db)
    return await Order_Pydantic.from_tortoise_orm(order_db)
