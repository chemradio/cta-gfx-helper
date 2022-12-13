import requests

from config import BACKUP_DB_ENDPONT, RESTORE_DB_ENDPONT


async def backup_db_request() -> None | dict:
    r = requests.get(BACKUP_DB_ENDPONT)
    result = r.json()
    if not result:
        return None
    return result


async def restore_db_request(db_backup: dict):
    r = requests.post(RESTORE_DB_ENDPONT, json=db_backup)
    return r.json()
