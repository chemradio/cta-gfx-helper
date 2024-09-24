from io import BytesIO

from starlette.datastructures import UploadFile


class AssetFile:
    def __init__(self, upload_file: UploadFile):
        self.filename = upload_file.filename
        self.file = BytesIO(upload_file.file.read())
