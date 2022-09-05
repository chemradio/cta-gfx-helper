from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os
import interlinks
from multiprocessing import Process, freeze_support

def start_httpd(directory: Path = interlinks.HTML_ASSEMBLIES_FOLDER, port: int = 8000):
    # print(f"serving from {directory}...")
    handler = partial(SimpleHTTPRequestHandler, directory=directory)
    httpd = HTTPServer(('localhost', port), handler)
    httpd.serve_forever()


def create_server() -> Process:
    server_process = Process(target=start_httpd)
    server_process.start()
    # return server_process


if __name__ == "__main__":
    create_server()
