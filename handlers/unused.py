from handlers.decorators import log_decorator
import interlinks
from engines.telegram_bot.bot_instance import bot

@log_decorator
def check_admin_id(user_id):
    if user_id in interlinks.admin_telegram_ids:
        return True
    else:
        bot.send_message(chat_id=user_id, text="Ошибка.")
        return False
