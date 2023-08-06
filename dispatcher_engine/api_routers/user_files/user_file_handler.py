import requests
from config import STORAGE_UNIT_URL
from fastapi import APIRouter, HTTPException, UploadFile
from utils.assets.file_convert.file_convert import (
    convert_unsupported_file,
    generate_random_filename,
)

router = APIRouter()


@router.post("/")
async def add_user_file(
    upload_file: UploadFile,
):
    # check file type and convert file if neccessary
    native_support_mimes = [
        "image/jpeg",
        "image/png",
        "audio/wav",
        "audio/x-wav",
        "audio/mpeg",
        "audio/mp3",
    ]

    if upload_file.content_type not in native_support_mimes:
        try:
            filename, file_bytes = await convert_unsupported_file(upload_file)
        except Exception as e:
            raise HTTPException(400, f"Bad file. {str(e)}")
    else:
        filename = generate_random_filename(
            extension=upload_file.filename.split(".")[-1]
        )
        file_bytes = upload_file.file.read()

    # store file in the storage unit
    response = requests.post(
        STORAGE_UNIT_URL,
        files={"upload_file": (filename, file_bytes)},
        # data={"category": "screenshots"},
    )
    response.raise_for_status()
    return {"filename": filename}
