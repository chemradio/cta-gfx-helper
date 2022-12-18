from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


def create_volume_folders():
    volume_path = Path().cwd() / "volume"

    children = (
        "cookie_file",
        "html_assemblies",
        "screenshots",
        "user_files",
        "video_exports",
    )
    children_paths = [volume_path / child for child in children]
    for child_path in children_paths:
        child_path.mkdir(parents=True, exist_ok=True)


create_volume_folders()

SERVER_URL = "0.0.0.0"
SERVER_PORT = 9006


def start_httpd(
    directory: Path = "./volume", url: str = SERVER_URL, port: int = SERVER_PORT
):
    handler = partial(SimpleHTTPRequestHandler, directory=directory)
    httpd = HTTPServer((url, port), handler)
    httpd.serve_forever()


if __name__ == "__main__":
    print("starting html server")
    start_httpd()
