from db_mongo.db_config.db_init import Users


def find_user(
    user_id: str | None = None,
    email: str | None = None,
    telegram_id: int | None = None,
    order: dict | None = None,
) -> dict | None:
    query = None
    if user_id:
        query = {"id": user_id}
    elif email:
        query = {"email": email}
    elif telegram_id:
        query = {"telegram_id": telegram_id}
    elif order:
        return find_user(
            user_id=order.get("user_id"),
            email=order.get("email"),
            telegram_id=order.get("telegram_id"),
        )

    if not query:
        return None
    return Users.find_one(query)
