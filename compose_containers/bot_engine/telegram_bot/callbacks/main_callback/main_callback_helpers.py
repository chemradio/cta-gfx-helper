from telegram import Update

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


def parse_user_first_name(update: Update) -> str:
    first_name = None
    try:
        return update.message.from_user.first_name
    except:
        # user id is not in message
        pass

    try:
        return update.callback_query.from_user.first_name
    except:
        # user id not in callback query
        pass

    return first_name
