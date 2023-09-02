import requests

from config import DISPATCHER_STRING_PROCESSOR_ENDPOINT


async def process_quote_string(quote_string: str) -> bool:
    r = requests.post(
        DISPATCHER_STRING_PROCESSOR_ENDPOINT, json={"quote_string": quote_string}
    )
    r.raise_for_status()
    return r.json().get("processed_string")
