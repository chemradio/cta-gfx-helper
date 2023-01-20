import secrets

import config
from fastapi import UploadFile


def save_user_file_to_volume(file: UploadFile = None) -> str:
    """Save a UploadFile instance to VOLUME and return new filename"""
    temp_name = f"user_{secrets.token_hex(8)}"
    extension = file.filename.split(".")[-1]
    full_filename = f"{temp_name}.{extension}"
    save_path = config.USER_FILES_FOLDER / full_filename
    with open(save_path, "wb+") as output_file:
        output_file.write(file.file.read())
    return full_filename
