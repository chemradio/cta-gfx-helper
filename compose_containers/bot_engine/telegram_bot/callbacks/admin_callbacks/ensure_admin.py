from py_gfxhelper_lib.user_enums.user_role import UserRole
from container_interaction.users import get_user_role


async def ensure_admin(telegram_id: int) -> bool:
    return await get_user_role(telegram_id) == UserRole.ADMIN
