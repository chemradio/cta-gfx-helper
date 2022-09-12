from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread
import interlinks

SERVER_URL = interlinks.ASSET_SERVER_URL
SERVER_PORT = interlinks.ASSET_SERVER_PORT

def start_httpd(directory: Path = './assets', url: str=SERVER_URL, port: int = SERVER_PORT):
    handler = partial(SimpleHTTPRequestHandler, directory=directory)
    httpd = HTTPServer((url, port), handler)

    def serve_forever(httpd):
        with httpd:  # to make sure httpd.server_close is called
            httpd.serve_forever()

    thread = Thread(target=serve_forever, args=(httpd, ), daemon=True)
    thread.start()


if __name__ == "__main__":
    start_httpd()
