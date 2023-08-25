from db_tortoise.helper_enums import OrderRequestType, OrderSource
from fastapi import Form, UploadFile
from pydantic import BaseModel, HttpUrl
from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator
from tortoise.models import Model


class Order(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="orders")

    # main description
    status = fields.CharField(max_length=100, null=True)
    request_type = fields.CharEnumField(enum_type=OrderRequestType, null=False)
    current_stage = fields.CharField(max_length=100, null=True)
    error = fields.BooleanField(default=False)
    error_type = fields.CharField(max_length=300, null=True, default="")

    ordered_from = fields.CharEnumField(enum_type=OrderSource)
    order_start_timestamp = fields.DatetimeField(null=True)
    order_creation_end_timestamp = fields.DatetimeField(auto_now_add=True)

    link = fields.CharField(max_length=700, null=True)
    link_type = fields.CharField(max_length=100, null=True)
    background_screenshot = fields.BooleanField(default=False)
    background_link = fields.CharField(max_length=200, null=True)

    # screenshots / static images
    screenshots_ready = fields.BooleanField(default=False)

    # video description
    is_two_layer = fields.BooleanField(default=False)
    fg_enabled = fields.BooleanField(default=False)
    background_name = fields.CharField(max_length=50, null=True)
    foreground_name = fields.CharField(max_length=50, null=True)
    bg_animation = fields.CharField(max_length=10, null=True)
    fg_animation = fields.CharField(max_length=10, null=True)

    video_gfx_name = fields.CharField(max_length=50, null=True)
    video_gfx_ready = fields.BooleanField(default=False)
    audio_name = fields.CharField(max_length=50, null=True)
    audio_enabled = fields.BooleanField(default=False)
    html_assembly_name = fields.CharField(max_length=50, null=True)

    send_success = fields.BooleanField(default=False)

    quote_enabled = fields.BooleanField(default=False)
    quote_text = fields.CharField(max_length=1000, null=True)
    quote_author_enabled = fields.BooleanField(default=False, null=True)
    quote_author_text = fields.CharField(max_length=100, null=True)

    # readtime
    readtime_result = fields.CharField(max_length=100, null=True)
    readtime_speed = fields.IntField(null=True)
    readtime_text = fields.CharField(max_length=1000, null=True)

    class Meta:
        table: str = "orders"

    class PydanticMeta:
        exclude = [
            "readtime_result",
        ]


class OrderIn_Pydantic(BaseModel):
    status: str | None = None
    request_type: str
    stage: str | None = None
    link: HttpUrl | None = None
    quote_enabled: bool | None = False
    quote_text: str | None = None
    quote_author_text: str | None = None
    quote_author_enabled: bool | None = None
    audio_enabled: bool | None = False
    audio_file: UploadFile | None = None
    foreground_file: UploadFile | None = None
    background_file: UploadFile | None = None
    ordered_from: str = "web"

    @classmethod
    def as_form(
        cls,
        status: str = Form(None),
        request_type: str = Form(...),
        stage: str | None = Form(None),
        link: HttpUrl | None = Form(None),
        quote_enabled: bool = Form(False),
        quote_text: str | None = Form(None),
        quote_author_text: str | None = Form(None),
        audio_enabled: bool = Form(False),
        audio_file: UploadFile | None = Form(None),
        foreground_file: UploadFile | None = Form(None),
        background_file: UploadFile | None = Form(None),
        ordered_from: str = Form("web"),
    ):
        return cls(
            status=status,
            request_type=request_type,
            stage=stage,
            link=link,
            quote_enabled=quote_enabled,
            quote_text=quote_text,
            quote_author_text=quote_author_text,
            audio_enabled=audio_enabled,
            audio_file=audio_file,
            foreground_file=foreground_file,
            background_file=background_file,
            ordered_from=ordered_from,
        )


Order_Pydantic = pydantic_model_creator(Order, name="Order")
