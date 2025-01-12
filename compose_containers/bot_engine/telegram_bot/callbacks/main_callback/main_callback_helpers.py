from telegram import Update

# import callbacks


def parse_user_id(update: Update) -> int:
    update_dict = update.to_dict()
    message_user_id  = update_dict.get("message", {}).get("from", {}).get("id")
    callback_query_user_id = update_dict.get("callback_query", {}).get("from", {}).get("id")
    return message_user_id or callback_query_user_id or None


def parse_user_first_name(update: Update) -> str:
    update_dict = update.to_dict()
    message_user_first_name = update_dict.get("message", {}).get("from", {}).get("first_name")
    callback_query_user_first_name = update_dict.get("callback_query", {}).get("from", {}).get("first_name")
    return message_user_first_name or callback_query_user_first_name or None