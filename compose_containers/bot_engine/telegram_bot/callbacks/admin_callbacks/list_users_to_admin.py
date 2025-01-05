import json

from config import BOT_ADMIN
from py_gfxhelper_lib.user_enums.user_permission import UserPermission
from py_gfxhelper_lib.user_enums.user_role import UserRole
from container_interaction.users import fetch_users
from telegram_bot.bot_instance import bot
from telegram_bot.responders.main_responder import Responder


async def list_users_to_admin(permission: UserPermission) -> None:
    users_list = await fetch_users()
    target_user_group = [
        user for user in users_list if user["permission"] == permission.value
    ]
    if not target_user_group:
        return await Responder.register_admin.empty_users_list(BOT_ADMIN)

    for user in target_user_group:
        await Responder.register_admin.list_user(
            admin_id=BOT_ADMIN,
            user_status=permission,
            user_id=user["telegram_id"],
            first_name=user["first_name"],
        )


async def list_users_to_admin_raw():
    users_list = await fetch_users()
    return await bot.send_message(
        chat_id=BOT_ADMIN,
        text=str(users_list),
    )
