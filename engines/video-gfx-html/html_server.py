from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os
from multiprocessing import Process

def start_httpd(directory: Path = os.path.abspath('./html/html_assemblies'), port: int = 8000):
    # print(f"serving from {directory}...")
    handler = partial(SimpleHTTPRequestHandler, directory=directory)
    httpd = HTTPServer(('localhost', port), handler)
    httpd.serve_forever()


def create_server():
    server_process = Process(target=start_httpd)
    server_process.start()


if __name__ == "__main__":
    create_server()
