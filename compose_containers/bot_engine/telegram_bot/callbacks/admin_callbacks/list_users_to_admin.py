from config import BOT_ADMIN
from py_gfxhelper_lib.user_enums.user_permission import UserPermission
from container_interaction.users import fetch_users
from telegram_bot.bot_instance import bot
from telegram_bot.responders.main_responder import Responder


async def list_users_to_admin(permission: UserPermission) -> None:
    users_list = await fetch_users(permission)
    if not users_list:
        return await Responder.register_admin.empty_users_list(BOT_ADMIN)

    for user in users_list:
        await Responder.register_admin.list_user(
            admin_id=BOT_ADMIN,
            user_status=permission,
            user_id=user.get("telegram_id"),
            first_name=user.get("first_name"),
        )


async def list_users_to_admin_raw():
    users_list = await fetch_users()
    return await bot.send_message(
        chat_id=BOT_ADMIN,
        text=str(users_list),
    )
