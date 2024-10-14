screenshot_link: str = Form(None),
secret_key: str | None = None,
callback_url: str | None = None,
background_file: UploadFile = File(...),
foreground_file: UploadFile | None = File(None),
audio_file: UploadFile | None = File(None),
quote_enabled: bool = Form(False),
quote_text: str | None = Form(None),
quote_author_enabled: bool = Form(None),
quote_author_text: str | None = Form(None),
template: str | None = Form(None),
framerate: int | float = Form(config.DEFAULT_FRAMERATE),
audio_offset: float = Form(config.DEFAULT_AUDIO_OFFSET),
videogfx_tail: float = Form(config.DEFAULT_VIDEOGFX_TAIL),
animation_duration: float | int = Form(config.DEFAULT_ANIMATION_DURATION),




import requests
from pathlib import Path

url = "http://127.0.0.1:9004/"  # Change this to your actual FastAPI server URL


def new_slave_order(url:str, order_data:dict[str, str|Path]):
    # init post data
    data = {}
    files = {}

    # check if value is Path and open it
    for key, value in order_data.items():
        if not value:
            continue
        if isinstance(value, Path):
            files[key] = open(value, "rb")
        else:
            data[key] = value


    # make the POST request
    if files:
        response = requests.post(url, files=files, data=data)
    else:
        response = requests.post(url, data=data)

    print (response.status_code)
    # Print the response
    print(response.status_code)
    print(response.text)

    # Close the file handlers after the request is done
    for f in files.values():
        f.close()




def check_order(order_id: str):
    data = {"order_id": order_id}
    response = requests.get(url, json=data)

    return response.json()


print(check_order())
