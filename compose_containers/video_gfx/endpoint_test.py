import requests

# The URL of your FastAPI endpoint
url = "http://127.0.0.1:9004/"  # Change this to your actual FastAPI server URL


def add_order():
    # The files to be uploaded
    files = {
        "background_file": open(
            "/Users/timurtimaev/Desktop/00.jpg", "rb"
        ),  # Replace with your actual file path
        "foreground_file": open(
            # "/Users/timurtimaev/Desktop/01.jpg", "rb"
            "/Users/timurtimaev/Desktop/02.jpg",
            "rb",
        ),  # Optional file
        "audio_file": open(
            "/Users/timurtimaev/Desktop/test_audio.mp3", "rb"
        ),  # Optional file
    }

    # The other form data (optional)
    data = {
        "quote_enabled": "true",
        "quote_text": "This is a sample quote.",
        "quote_author_enabled": "true",
        "quote_author_text": "Author Name",
        # "template": "Template1",
        # "framerate": 12,
        # "audio_offset": 1.5,
        # "videogfx_tail": 2.0,
    }

    # Make the POST request
    response = requests.post(url, files=files, data=data)

    # Print the response
    print(response.status_code)
    print(response.text)

    # Close the file handlers after the request is done
    for f in files.values():
        f.close()


# add_order()


def check_order(order_id: str):
    data = {"order_id": order_id}
    response = requests.get(url, json=data)

    return response.json()


print(check_order())
