def vitaly_user_converter(user_dict: dict) -> dict:
    return {
        "email": user_dict.get("email"),
        "password": None,
        "token": None,
        "confirmationCode": None,
        "role": None,
        "username": user_dict.get("username"),
        "avatar": None,
    }


def vitaly_order_converter(order_dict: dict) -> dict:
    return {
        "stage": order_dict.get("stage"),
        "status": order_dict.get("status"),
        "request_type": order_dict.get("request_type"),
        "quote_enabled": order_dict.get("quote_enabled"),
        "audio_enabled": order_dict.get("audio_enabled"),
        "quote_text": order_dict.get("quote_text"),
        "quote_author_text": order_dict.get("quote_author_text"),
        "quote_author_enabled": order_dict.get("quote_author_enabled"),
        "ordered_from": "web",
        "audio_name": order_dict.get("audio_name"),
        "background_name": order_dict.get("background_name"),
        "foreground_name": order_dict.get("foreground_name"),
        "fg_enabled": order_dict.get("fg_enabled"),
        "order_start_timestamp": order_dict.get("order_start_timestamp"),
        "order_creation_end_timestamp": order_dict.get("order_creation_end_timestamp"),
        "link": order_dict.get("link"),
        "readtime_speed": order_dict.get("readtime_speed"),
        "readtime_text": order_dict.get("readtime_text"),
        "user_email": order_dict.get("user_email"),
    }
