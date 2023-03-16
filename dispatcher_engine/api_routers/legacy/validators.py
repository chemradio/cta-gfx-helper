import re

from fastapi import APIRouter, HTTPException

router = APIRouter()

# orders
@router.post("/validate_link")
def add_order(request: dict):
    link = request.get("link")
    if not link:
        raise HTTPException(status_code=400, detail="Not a valid link")
    validation_result = check_is_url(link)
    if not validation_result:
        raise HTTPException(status_code=400, detail="Not a valid link")

    return True


def check_is_url(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]
