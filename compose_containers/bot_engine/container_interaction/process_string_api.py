import httpx
from config import TEXT_PROCESSOR_ENDPOINT


async def process_quote_string(quote_string: str) -> str:
    async with httpx.AsyncClient() as client:
        r = await client.post(TEXT_PROCESSOR_ENDPOINT, json={"text": quote_string})
        r.raise_for_status()
        return r.json().get("processed_string")
