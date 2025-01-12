from py_gfxhelper_lib.files.asset_file import AssetFile
import httpx

async def convert_user_file(file: AssetFile) -> AssetFile:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            "http://file_converter:9005", files={"file": (file.filename, file.bytesio, file.mime_type)}
        )
        r.raise_for_status()

    return AssetFile(bytes_or_bytesio=r.content, mime_type=r.headers["Content-Type"])