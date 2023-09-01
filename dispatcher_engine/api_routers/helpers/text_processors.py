from fastapi import APIRouter, Request
from pydantic import BaseModel

from utils.text.quote_preprocessor import preprocess_string


class TextInput(BaseModel):
    quote_string: str


router = APIRouter()


@router.post("/")
async def process_quote_string(
    text_input: TextInput,
):
    return {"processed_string": preprocess_string(text_input.quote_string)}
