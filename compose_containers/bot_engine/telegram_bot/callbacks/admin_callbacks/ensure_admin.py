from py_gfxhelper_lib.user_enums.user_role import UserRole
from container_interaction.users import check_user_role_admin


async def ensure_admin(telegram_id: int) -> bool:
    return await check_user_role_admin(telegram_id)
