from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator
from tortoise.models import Model

from db_tortoise.helper_enums import SystemEventType


class SystemEvent(Model):
    id = fields.IntField(pk=True)
    type = fields.CharEnumField(enum_type=SystemEventType)
    description = fields.CharField(max_length=200, null=True)
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table: str = "system_events"


SystemEvent_Pydantic = pydantic_model_creator(SystemEvent, name="SystemEvent")
