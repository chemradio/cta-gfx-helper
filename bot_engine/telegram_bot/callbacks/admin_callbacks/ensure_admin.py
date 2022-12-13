from container_interaction.users_db import (
    check_user_status,
)
from container_interaction.helpers import UserStatus
from container_interaction.users_db import check_user_status


async def ensure_admin(telegram_id: int) -> bool:
    user_status = await check_user_status(telegram_id)
    if user_status == UserStatus.ADMIN:
        return True
    else:
        return False
