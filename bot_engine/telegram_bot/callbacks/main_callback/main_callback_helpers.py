from telegram import Update

from telegram_bot.responders.bot_texts import Responses

# import callbacks


def parse_user_id(update: Update) -> int:
    user_id = None
    try:
        return update.message.from_user.id
    except:
        # user id is not in message
        pass

    try:
        return update.callback_query.from_user.id
    except:
        # user id not in callback query
        pass

    return user_id


def get_user_auth_status(user_id: int) -> None:
    pass
