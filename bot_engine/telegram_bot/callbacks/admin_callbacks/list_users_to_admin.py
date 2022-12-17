from config import BOT_ADMIN
from container_interaction.helpers import UserStatus
from container_interaction.users_db import fetch_users
from telegram_bot.responders.main_responder import Responder


async def list_users_to_admin(type: UserStatus) -> None:
    users_list = await fetch_users()
    target_user_group = [user for user in users_list if user["status"] == type.value]
    if not target_user_group:
        return await Responder.register_admin.empty_users_list(BOT_ADMIN)

    for user in target_user_group:
        await Responder.register_admin.list_user(
            admin_id=BOT_ADMIN,
            user_status=type,
            user_id=user["telegram_id"],
            first_name=user["first_name"],
        )