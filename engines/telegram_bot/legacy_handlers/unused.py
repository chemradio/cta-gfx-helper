from engines.telegram_bot.legacy_handlers.decorators import log_decorator
import interlinks
from engines.telegram_bot.bot_instance import bot

@log_decorator
def check_admin_id(user_id):
    if user_id in interlinks.ADMIN_TELEGRAM_IDS:
        return True
    else:
        bot.send_message(chat_id=user_id, text="Ошибка.")
        return False
