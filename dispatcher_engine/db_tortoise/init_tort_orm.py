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


async def list_tables():
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

    conn = Tortoise.get_connection("default")
    table_names = await conn.execute_query_dict(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    )
    table_names = [table["table_name"] for table in table_names]
    return table_names


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
