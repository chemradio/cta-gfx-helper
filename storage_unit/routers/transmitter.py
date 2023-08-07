from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from utils.assets.asset_finder import find_file

router = APIRouter()


@router.get("/file")
async def get_file(filename: str):
    print("Request for retrieving file from the storage unit.")
    print(f"Filename: {filename}")

    search = find_file(filename)
    if not search:
        raise HTTPException(404, f"File *{filename}* not found")

    return FileResponse(search[0])
