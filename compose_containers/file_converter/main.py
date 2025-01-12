from io import BytesIO

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import Response, FileResponse
from py_gfxhelper_lib.files.asset_file import AssetFile
from workflows.file_convert import convert_unsupported_file

app = FastAPI()


@app.post("/")
async def convert_file(
    file: UploadFile = File(...),
):
    try:
        converted_file = await convert_unsupported_file(
            AssetFile(bytes_or_bytesio=file.file.read(), extension=file.filename.split(".")[-1])
        )

        return Response(
            content=converted_file.bytesio.getvalue(),
            media_type=converted_file.mime_type,
        )
    except Exception as e:
        print("Conversion error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
