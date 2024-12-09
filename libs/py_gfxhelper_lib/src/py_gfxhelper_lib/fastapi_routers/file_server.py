from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()


def find_asset(filename: str, search_path: Path = Path.cwd() / "storage") -> Path:
    return next(search_path.rglob(filename), None)


@router.get("/file_server")
async def download_file(filename: str):
    file_path = find_asset(filename)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, filename=file_path.name)


@router.delete("/file_server")
async def delete_file(filename: str):
    file_path = find_asset(filename)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")

    file_path.unlink()
    return {"status": "deleted", "filename": file_path.name}
