from io import BytesIO

from starlette.datastructures import UploadFile


class AssetFile:
    def __init__(
        self,
        upload_file: UploadFile | None = None,
        filename: str | None = None,
        file: BytesIO | None = None,
    ):
        if upload_file:
            self.filename = upload_file.filename
            self.file = BytesIO(upload_file.file.read())
        else:
            self.filename = filename
            self.file = file


BytesIO()
