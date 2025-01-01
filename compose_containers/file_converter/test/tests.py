import httpx
import asyncio

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


async def submit_file_conversion(file_path: Path):
    async with httpx.AsyncClient() as client:
        return await client.post(
            "http://127.0.0.1:9005", files={"file": file_path.open("rb")}
        )


async def seq_test_file_conversion():
    # iterate over each file in test/to_convert
    for file_path in Path("test/to_convert").iterdir():
        result = await submit_file_conversion(file_path)
        # print result file mime type
        converted_extension = mime_map[result.headers["Content-Type"]]
        with open(f"test/converted/{file_path.stem}.{converted_extension}", "wb") as f:
            f.write(result.content)


async def main():
    from time import perf_counter

    start = perf_counter()
    await seq_test_file_conversion()
    end = perf_counter()


if __name__ == "__main__":
    asyncio.run(main())
