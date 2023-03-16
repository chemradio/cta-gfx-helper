from json import JSONDecodeError

from fastapi import Request


async def request_json_parser(request: Request):
    try:
        return await request.json()
    except JSONDecodeError:
        return None
