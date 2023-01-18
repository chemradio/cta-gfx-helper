from typing import Optional, Union

from fastapi import APIRouter, File, UploadFile

router = APIRouter()

# orders
@router.post("/test_download")
def add_order(files: list[UploadFile] | None = None):
    returns = list()
    return files, type(files)

    # # returns = [
    # #     request if request else None,
    # # ]

    # i = 0
    # for file in files:
    #     file_contents = file.read()
    #     with open(f"test_file_{i}.txt", "wb") as f:
    #         f.write(file_contents)
    #         returns.append(file.filename)
    #         i += 1
    # return returns
