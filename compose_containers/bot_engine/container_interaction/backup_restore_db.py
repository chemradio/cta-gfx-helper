import httpx

from config import BACKUP_DB_ENDPONT, RESTORE_DB_ENDPONT


async def backup_db_request() -> None | dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(BACKUP_DB_ENDPONT)
        return r.json()


async def restore_db_request(db_backup: dict) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.post(RESTORE_DB_ENDPONT, json=db_backup)
        return r.json()
