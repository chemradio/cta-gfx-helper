from typing import Optional

import requests

from config import USERS_ENDPOINT


def get_one_user(user_id: str) -> Optional[list]:
    r = requests.get(
        USERS_ENDPOINT,
        json={"id": user_id},
    )
    result = r.json()
    return result
