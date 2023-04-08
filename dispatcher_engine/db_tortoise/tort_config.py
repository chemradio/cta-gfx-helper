import config

TORTOISE_ORM = {
    "connections": {"default": config.DB_CONNECTION_STRING},
    "apps": {
        "user": {
            "models": [
                "db_tortoise.users_models",
                "db_tortoise.orders_models",
                "db_tortoise.system_events_models",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}
