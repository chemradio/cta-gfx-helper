from container_interaction.helpers import UserRole
from container_interaction.users_db import check_user_role_admin


async def ensure_admin(telegram_id: int) -> bool:
    return await check_user_role_admin(telegram_id)
