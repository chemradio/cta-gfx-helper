import asyncio

from db_tortoise.init_tort_orm import rebuild_tortoise_postgres

asyncio.run(rebuild_tortoise_postgres())
