from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


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


def preprocess_string(string: str) -> str:
    string = (
        string.strip()
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\t\t", "\t")
        .replace("\t\t", "\t")
        .replace("\t\t", "\t")
        .replace("\n\t", "\n")
        .replace("\t", "\n")
        # .replace("\n", " <...> ")
        .replace(" <...> <...> ", " <...> ")
        .replace(" <...> <...> ", " <...> ")
        .replace("Ë", "Е")
        .replace("ё", "е")
        .replace("«", '"')
        .replace("»", '"')
        .replace(" - ", " – ")
    )

    if "  " in string:
        string = string.replace("  ", " ")

    return string
