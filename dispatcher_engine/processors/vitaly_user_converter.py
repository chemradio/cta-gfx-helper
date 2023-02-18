def vitaly_converter(user_dict: dict) -> dict:
    return {
        "email": user_dict.get("email"),
        "password": None,
        "token": None,
        "confirmationCode": None,
        "role": None,
        "username": user_dict.get("username"),
        "avatar": None,
    }
