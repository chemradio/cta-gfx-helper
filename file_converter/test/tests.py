import httpx
import asyncio

from pathlib import Path
from workflows.helper_types import mime_map


async def submit_file_conversion(file_path: Path):
    async with httpx.AsyncClient() as client:
        return await client.post(
            "http://127.0.0.1:8000", files={"file": file_path.open("rb")}
        )


async def seq_test_file_conversion():
    # iterate over each file in test/to_convert
    for file_path in Path("test/to_convert").iterdir():
        print("converting file:", file_path)
        result = await submit_file_conversion(file_path)
        # print result file mime type
        print(result)
        print(result.headers["Content-Type"])

        converted_extension = mime_map[result.headers["Content-Type"]]
        with open(f"test/converted/{file_path.stem}.{converted_extension}", "wb") as f:
            f.write(result.content)


async def async_test_file_conversion():
    # iterate over each file in test/to_convert
    tasks = []
    for file_path in Path("test/to_convert").iterdir():
        print("converting file:", file_path)
        tasks.append(submit_file_conversion(file_path))
    results = await asyncio.gather(*tasks)
    for result in results:
        # print result file mime type
        print(result)
        print(result.headers["Content-Type"])

        converted_extension = mime_map[result.headers["Content-Type"]]
        with open(f"test/converted/{file_path.stem}.{converted_extension}", "wb") as f:
            f.write(result.content)


async def main():
    from time import perf_counter

    start = perf_counter()
    await seq_test_file_conversion()
    end = perf_counter()
    print("Sequential time:", end - start)

    start = perf_counter()
    await async_test_file_conversion()
    end = perf_counter()
    print("Async time:", end - start)


if __name__ == "__main__":
    asyncio.run(main())
