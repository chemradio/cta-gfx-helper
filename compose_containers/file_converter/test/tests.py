import httpx
import asyncio
from py_gfxhelper_lib.intercontainer_requests.file_requests import convert_file
from py_gfxhelper_lib.files.asset_file import AssetFile
from pathlib import Path

mime_map = {
    "application/pdf": "pdf",
    "image/png": "png",
    "image/jpeg": "jpg",
    "audio/wav": "wav",
    "audio/mpeg": "mp3",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
}

async def test_file_conversion():
    # iterate over each file in test/to_convert
    audio_path = Path.cwd() / "test.mp3"
    with open(audio_path, 'rb') as f:
        file_bytes = f.read()
    orig_file = AssetFile(bytes_or_bytesio=file_bytes, extension='mp3')
    result = await convert_file(orig_file, file_converter_url="http://127.0.0.1:9005")
    print(result)
    print(result.filename)
    print(result.mime_type)
    print(result.extension)
    with open(Path.cwd() /result.filename, "wb") as f:
        f.write(result.bytesio.getvalue())


# async def submit_file_conversion(file_path: Path):
#     async with httpx.AsyncClient() as client:
#         return await client.post(
#             "http://127.0.0.1:9005", files={"file": file_path.open("rb")}
#         )


# async def seq_test_file_conversion():
#     # iterate over each file in test/to_convert
#     for file_path in Path("test/to_convert").iterdir():
#         result = await submit_file_conversion(file_path)
#         # print result file mime type
#         converted_extension = mime_map[result.headers["Content-Type"]]
#         with open(f"test/converted/{file_path.stem}.{converted_extension}", "wb") as f:
#             f.write(result.content)



async def main():
    # from time import perf_counter
    await test_file_conversion()
    # start = perf_counter()
    # await seq_test_file_conversion()
    # end = perf_counter()


if __name__ == "__main__":
    asyncio.run(main())
