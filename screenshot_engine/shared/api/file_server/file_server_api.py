import fastapi
from pathlib import Path
from shared.api.file_server.api_input_classes import FileRequest


router = fastapi.APIRouter()


@router.get("/file")
async def download_file(file_request: FileRequest):
    file_path = find_asset(file_request.filename)
    if not file_path:
        raise fastapi.HTTPException(status_code=404, detail="File not found")

    return fastapi.responses.FileResponse(file_path, filename=file_path.name)


@router.delete("/file")
async def delete_file(file_request: FileRequest):
    file_path = find_asset(file_request.filename)
    if not file_path:
        raise fastapi.HTTPException(status_code=404, detail="File not found")

    file_path.unlink()
    return {"status": "deleted", "filename": file_path.name}


def find_asset(filename: str, search_path: Path = Path.cwd() / "storage") -> Path:
    return next(search_path.rglob(filename), None)
