import httpx
from config import DISPATCHER_STRING_PROCESSOR_ENDPOINT


async def process_quote_string(quote_string: str) -> str:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            DISPATCHER_STRING_PROCESSOR_ENDPOINT, json={"quote_string": quote_string}
        )
        r.raise_for_status()
        return r.json().get("processed_string")
