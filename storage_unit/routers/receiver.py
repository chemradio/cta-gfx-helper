from fastapi import APIRouter, Form, UploadFile

import config

router = APIRouter()


@router.post("/")
async def store_file(upload_file: UploadFile, category: str | None = Form(None)):
    print(category)
    with open(config.DEFAULT_PATH / upload_file.filename, "wb+") as f:
        f.write(upload_file.file.read())

    return f"File {upload_file.filename} was stored"
