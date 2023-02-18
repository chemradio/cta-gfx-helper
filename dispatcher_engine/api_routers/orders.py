import os
import time
from pprint import pprint

from fastapi import APIRouter, BackgroundTasks, Form, Request, UploadFile

from api_routers.signal_sender import signal_to_services
from db.sql_handler import db
from processors.cleanup_order_assets import cleanup_order_assets
from processors.orders import advance_order_stage
from processors.save_user_file_to_volume import save_user_file_to_volume

router = APIRouter()

# orders
@router.post("/add_order_telegram")
def add_order(order: dict, background_tasks: BackgroundTasks):
    order["ordered_from"] = "telegram"
    order = advance_order_stage(order)
    db.add_order(**order)
    background_tasks.add_task(signal_to_services, order.get("current_stage"))
    return True


@router.post("/add_order_web")
async def add_order_web(
    # request: Request,
    background_tasks: BackgroundTasks,
    # global request type
    requestType: str = Form(None),
    # quote
    quoteEnabled: bool = Form(False),
    quoteTextText: str = Form(None),
    quoteAuthorText: str = Form(None),
    # audio file
    audioEnabled: bool = Form(False),
    audioFile: UploadFile | None = None,
    # link
    videoAutoLink: str = Form(None),
    # custom layers
    videoFilesPrimaryDocument: UploadFile | None = None,
    videoFilesBackgroundDocument: UploadFile | None = None,
):
    # # print(dir(request))
    # # print(await request.body())
    # # x = request.items()
    # x = await request.form()
    # print(x)

    # inititalize empty order
    order = dict()
    order["ordered_from"] = "web"

    # testing purposes only
    order["telegram_id"] = os.environ.get("BOT_ADMIN")

    # placeholder epoch timestamp values
    order["order_start_timestamp"] = int(time.time())
    order["order_creation_end_timestamp"] = int(time.time())

    # parse request type
    # request_type_map = {"videoAuto": "video_auto", "videoFiles": "video_files"}
    # order["request_type"] = request_type_map[requestType]

    order["request_type"] = "video_auto"

    # parse quote settings
    order["quote_enabled"] = quoteEnabled
    if quoteEnabled:
        order["quote_author_enabled"] = True
        order["quote_text"] = quoteTextText
        order["quote_author_text"] = quoteAuthorText

    # to be implemented
    order["audio_enabled"] = audioEnabled
    if audioEnabled:
        # download file first
        audio_name = save_user_file_to_volume(audioFile)
        order["audio_name"] = audio_name

    if order["request_type"] == "video_auto":
        order["link"] = videoAutoLink

    if order["request_type"] == "video_files":
        primary_document = ""
        background_document = ""

        if videoFilesPrimaryDocument:
            primary_document = save_user_file_to_volume(videoFilesPrimaryDocument)
        if videoFilesBackgroundDocument:
            background_document = save_user_file_to_volume(videoFilesBackgroundDocument)

        if background_document:
            order["background_name"] = background_document
            order["foreground_name"] = primary_document
        else:
            order["background_name"] = primary_document
            order["foreground_name"] = ""

    # signal
    order = advance_order_stage(order)
    db.add_order(**order)
    background_tasks.add_task(signal_to_services, order.get("current_stage"))

    return True


@router.post("/edit")
def edit_order(order: dict, background_tasks: BackgroundTasks):
    print("edit order initiated")
    print(f"input data: {order=}")
    order = advance_order_stage(order)
    if not db.edit_order(**order):
        return False

    print(f"advanced order: {order=}")

    order_status = order.get("status")
    if order_status == "completed":
        try:
            cleanup_order_assets(order)
        except Exception as e:
            print("Error in edit order. strange")
            print(e)

    print(f"after cleaning assets")

    current_stage = order.get("current_stage")
    background_tasks.add_task(signal_to_services, current_stage)
    print("after starting bg task")
    return True


@router.post("/truncate")
def truncate_orders():
    db.truncate_orders()
    return True


@router.get("/list")
def list_orders(request: dict = {}):
    """Returns a list of all orders if not specified."""
    status = request.get("status")
    orders = db.list_orders(status)

    for order in orders:
        user = db.find_user_by_telegram_id(order.user_telegram_id)
        order.user_first_name = user.first_name

    return {"orders": orders}


@router.get("/get_one")
def get_one(request: dict):
    """Returns a list of all users if not specified."""
    current_stage = request.get("current_stage")

    request_status = request.get("status")
    status = request_status if request_status else "active"

    order = db.get_one_order(current_stage, status)
    if not order:
        return None

    # generate and cleanup the order dict
    order_dict = order.__dict__
    order_dict.pop("_sa_instance_state")
    print("get_one_log")
    print(f"{order_dict=}")
    updated_order = advance_order_stage(order_dict)
    print(f"{updated_order=}")
    db.edit_order(**updated_order)
    return order
