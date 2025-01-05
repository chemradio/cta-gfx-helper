from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from py_gfxhelper_lib.miscellaneous.string_cleaner import cleanup_string

class TextInput(BaseModel):
    quote_string: str


router = APIRouter()


@router.post("/")
async def process_quote_string(
    text: TextInput,
):
    if len(text.quote_string) < 1:
        raise HTTPException(400, "Текст слишком короткий")

    return {"processed_string": cleanup_string(text.quote_string)}

