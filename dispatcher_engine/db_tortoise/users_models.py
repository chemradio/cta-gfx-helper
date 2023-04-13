from fastapi import Form
from pydantic import BaseModel, EmailStr
from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator
from tortoise.models import Model

from db_tortoise.helper_enums import NormalUserPermission, UserRole


class User(Model):
    id = fields.IntField(pk=True)

    first_name = fields.CharField(max_length=100, null=True)
    username = fields.CharField(max_length=100, null=True)
    telegram_id = fields.BigIntField(null=True, unique=True)
    email = fields.CharField(max_length=100, unique=True)

    created = fields.DatetimeField(auto_now_add=True)
    password_hash = fields.CharField(max_length=200, null=True)
    role = fields.CharEnumField(
        enum_type=UserRole, max_length=15, default=UserRole.NORMAL.value, null=True
    )
    permission = fields.CharEnumField(
        enum_type=NormalUserPermission,
        default=NormalUserPermission.PENDING.value,
        max_length=15,
    )

    description = fields.CharField(max_length=100, null=True)
    status = fields.CharField(max_length=100, null=True)
    current_stage = fields.CharField(max_length=100, null=True)

    class Meta:
        table: str = "users"

    class PydanticMeta:
        exclude = ["password_hash"]


class UserIn_Pydantic(BaseModel):
    username: str | None = None
    email: EmailStr
    password: str
    passphrase: str | None = None

    @classmethod
    def as_form(
        cls,
        username: str | None = Form(None),
        email: EmailStr = Form(...),
        password: str = Form(...),
        passphrase: str | None = Form(None),
    ):
        print(username, email, password, passphrase)
        return cls(
            username=username, email=email, password=password, passphrase=passphrase
        )


User_Pydantic = pydantic_model_creator(User, name="User", exclude=("password_hash",))
