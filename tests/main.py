import httpx


with httpx.Client() as client:
    response = client.get(
        "http://127.0.0.1:9002/file_server/", params={"filename": "nGNT0SGI.png"}
    )
    with open("temp.png", "wb") as f:
        f.write(response.content)
