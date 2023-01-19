import time

from fastapi import APIRouter, BackgroundTasks, Form, UploadFile

from api_routers.signal_sender import signal_to_services
from db.sql_handler import db
from processors.orders import advance_order_stage

router = APIRouter()

# orders
@router.post("/add_order")
async def add_order(
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
    order = dict()
    order["order_start_timestamp"] = int(time.time())
    order["order_creation_end_timestamp"] = int(time.time())

    # parse request type
    request_type_map = {"videoAuto": "video_auto", "videoFiles": "video_files"}
    order["request_type"] = request_type_map[requestType]

    order["quote_enabled"] = quoteEnabled
    if quoteEnabled:
        order["quote_author_enabled"] = True
        order["quote_text"] = quoteTextText
        order["quote_author_text"] = quoteAuthorText

    # to be implemented
    order["audio_enabled"] = audioEnabled
    if audioEnabled:
        order["audio_name"] = audioFile

    if order["request_type"] == "video_auto":
        order["link"] = videoAutoLink

    if order["request_type"] == "video_files":
        if videoFilesBackgroundDocument:
            order["background_name"] = videoFilesBackgroundDocument
            order["foreground_name"] = videoFilesPrimaryDocument
        else:
            order["background_name"] = videoFilesPrimaryDocument
            order["foreground_name"] = ""

    # signal
    order = advance_order_stage(order)
    db.add_order(**order)
    background_tasks.add_task(signal_to_services, order.get("current_stage"))

    return True
