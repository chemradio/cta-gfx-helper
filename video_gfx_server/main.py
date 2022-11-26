from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

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
