import asyncpg
from tortoise import Tortoise

from .tort_config import TORTOISE_ORM

DB_URL = TORTOISE_ORM["connections"]["default"]


async def drop_tables() -> None:
    # # sqlite
    # await Tortoise.init(db_url=DB_URL, modules={"models": ["db_tortoise.models"]})
    # await Tortoise._drop_databases()
    # await Tortoise.close_connections()
    conn = await asyncpg.connect(DB_URL)

    # first option - drop the while PUBLIC schema
    # Execute a statement to create a new table.
    await conn.execute("DROP SCHEMA public CASCADE")
    await conn.execute("CREATE SCHEMA public;")
    await conn.execute("GRANT ALL ON SCHEMA public TO postgres;")
    await conn.execute("GRANT ALL ON SCHEMA public TO public;")
    await conn.close()


async def create_tables() -> None:
    await Tortoise.init(
        db_url=DB_URL,
        modules={
            "models": [
                "db_tortoise.users_models",
                "db_tortoise.orders_models",
                "db_tortoise.system_events_models",
            ],
        },
    )
    await Tortoise.generate_schemas()


async def check_models_in_db() -> bool:
    await Tortoise.init(
        db_url=DB_URL,
        modules={
            "models": [
                "db_tortoise.users_models",
                "db_tortoise.orders_models",
                "db_tortoise.system_events_models",
            ],
        },
    )
    db_description = Tortoise.describe_models()
    models = ("Order", "User", "SystemEvent")
    for model in models:
        if f"models.{model}" not in db_description:
            return False
    return True


async def initialize_tortoise_postgres() -> None:
    models_ok = await check_models_in_db()
    if not models_ok:
        await drop_tables()
        await create_tables()


async def rebuild_tortoise_postgres() -> None:
    await drop_tables()
    await create_tables()
