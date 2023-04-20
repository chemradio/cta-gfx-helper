import asyncio
import sys

from db_tortoise.init_tort_orm import create_tables, drop_tables, list_tables


async def check_tables() -> bool:
    current_tables = await list_tables()
    return set(current_tables) == set(["users", "orders", "system_events"])


async def rebuild_db() -> None:
    await drop_tables()
    await create_tables()


async def main():
    tables_correct = await check_tables()
    if tables_correct:
        print("Tablenames match. Exiting...")
        return
    else:
        print("Rebuilding...")
        await rebuild_db()
        print("Done. Exiting")


if __name__ == "__main__":
    asyncio.run(main())
