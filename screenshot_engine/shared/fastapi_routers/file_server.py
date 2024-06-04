import fastapi
import pydantic
from pathlib import Path


router = fastapi.APIRouter()


class FileRequest(pydantic.BaseModel):
    filename: str
    secret_key: str | None = None


def find_asset(filename: str, search_path: Path = Path.cwd() / "storage") -> Path:
    return next(search_path.rglob(filename), None)


@router.get("/")
async def download_file(file_request: FileRequest):
    file_path = find_asset(file_request.filename)
    if not file_path:
        raise fastapi.HTTPException(status_code=404, detail="File not found")

    return fastapi.responses.FileResponse(file_path, filename=file_path.name)


@router.delete("/")
async def delete_file(file_request: FileRequest):
    file_path = find_asset(file_request.filename)
    if not file_path:
        raise fastapi.HTTPException(status_code=404, detail="File not found")

    file_path.unlink()
    return {"status": "deleted", "filename": file_path.name}
