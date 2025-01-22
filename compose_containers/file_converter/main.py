from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import Response
from py_gfxhelper_lib.files.asset_file import AssetFile
from workflows.converters.file_convert import convert_unsupported_file
from workflows.image_rescaler.image_rescale import rescale_image

app = FastAPI()


@app.post("/")
async def convert_file(
    file: UploadFile = File(...),
):
    try:
        converted_file = convert_unsupported_file(
            AssetFile(
                bytes_or_bytesio=file.file.read(),
                extension=file.filename.split(".")[-1],
            )
        )

        return Response(
            content=converted_file.bytesio.getvalue(),
            media_type=converted_file.mime_type,
        )
    except Exception as e:
        print("Conversion error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reduce_image/")
async def reduce_image(
    original_image: UploadFile = File(None),
    max_width: int | None = Form(None),
    max_height: int | None = Form(None),
):
    try:
        rescaled_image = await rescale_image(
            AssetFile(
                bytes_or_bytesio=original_image.file.read(),
                extension=original_image.filename.split(".")[-1],
            ),
            max_width=max_width,
            max_height=max_height,
        )

        return Response(
            content=rescaled_image.bytesio.getvalue(),
            media_type=rescaled_image.mime_type,
        )
    except Exception as e:
        print("Conversion error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
