from io import BytesIO

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import Response, FileResponse

from workflows.file_convert import convert_unsupported_file

app = FastAPI()


@app.post("/")
async def convert_file(
    file: UploadFile = File(...),
):
    try:
        original_extension = file.filename.split(".")[-1]
        file_bytesio = BytesIO(file.file.read())

        converted_file = await convert_unsupported_file(
            file_bytesio, original_extension
        )

        return Response(
            content=converted_file.bytesio.getvalue(),
            media_type=converted_file.mime_type,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
