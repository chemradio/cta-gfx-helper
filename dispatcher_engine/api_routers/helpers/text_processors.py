from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.text.quote_preprocessor import preprocess_string


class TextInput(BaseModel):
    quote_string: str


router = APIRouter()


@router.post("/")
async def process_quote_string(
    text: TextInput,
):
    if len(text.quote_string) < 1:
        raise HTTPException(400, "Текст слишком короткий")

    return {"processed_string": preprocess_string(text.quote_string)}
