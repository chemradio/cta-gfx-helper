from io import BytesIO
from .mime_extension_mapping import MIME_TO_EXTENSION, EXTENSION_TO_MIME
import random
import string


class AssetFile:
    def __init__(
        self,
        bytes: bytes | BytesIO,
        extension: str | None,
        mime_type: str | None,
        mime_map: dict[str, str] = MIME_TO_EXTENSION,
        extension_map: dict[str, str] = EXTENSION_TO_MIME,
    ):
        """Usable fields are: extension, bytesio, mime_type"""
        if extension is None and mime_type is None:
            raise ValueError("Either extension or mime_type must be provided")

        if bytes is None and bytesio is None:
            raise ValueError("Either bytes or bytesio must be provided")

        if extension is not None:
            self.extension = extension
            self.mime_type = extension_map[extension]
        else:
            self.mime_type = mime_type
            self.extension = mime_map[mime_type]

        if isinstance(bytes, bytes):
            self.bytesio = BytesIO(bytes)
        elif isinstance(bytes, BytesIO):
            self.bytesio = bytes

    @property
    def random_full_filename(self) -> str:
        """Return random filename of letters and numbers
        with a length of 8 characters with extension"""
        return (
            "".join(random.choices(string.ascii_letters + string.digits, k=8))
            + f".{self.extension}"
        )
