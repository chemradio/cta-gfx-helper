import requests
from fastapi import APIRouter, HTTPException, UploadFile

from config import STORAGE_UNIT_URL
from utils.assets.file_convert.file_convert import convert_unsupported_file
from utils.assets.filenames import (
    generate_random_filename,
    get_file_extension_from_mime,
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
            file_bytes = await convert_unsupported_file(upload_file)
        except Exception as e:
            print("Something went wrong")
            print(str(e))
            raise HTTPException(400, f"Bad file. {str(e)}")
    else:
        file_bytes = upload_file.file.read()

    filename = generate_random_filename(
        extension=get_file_extension_from_mime(upload_file.content_type)
    )

    # store file in the storage unit
    response = requests.post(
        STORAGE_UNIT_URL,
        files={"upload_file": (filename, file_bytes)},
    )
    response.raise_for_status()
    return {"filename": filename}
