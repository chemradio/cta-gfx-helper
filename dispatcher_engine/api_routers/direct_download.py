from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from processors.asset_finder import find_files

router = APIRouter()

# orders
@router.get("/direct_download/{filename}")
def direct_download(filename: str):
    target_file_list = find_files(filename)

    if not target_file_list:
        raise HTTPException(status_code=404, detail="File not found.")

    return FileResponse(
        path=target_file_list[0],
        status_code=200,
        filename=filename,
    )
