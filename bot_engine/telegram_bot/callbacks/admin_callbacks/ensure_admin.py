from container_interaction.helpers import UserRole
from container_interaction.users_db import check_user_role, check_user_status


async def ensure_admin(telegram_id: int) -> bool:
    user_role = await check_user_role(telegram_id)
    if user_role == UserRole.ADMIN:
        return True
    else:
        return False
