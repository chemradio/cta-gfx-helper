from io import BytesIO
from .mime_extension_mapping import MIME_TO_EXTENSION, EXTENSION_TO_MIME
import random
import string


class AssetFile:
    def __init__(
        self,
        bytes_or_bytesio: bytes | BytesIO,
        extension: str | None,
        mime_type: str | None,
        mime_to_ext_map: dict[str, str] = MIME_TO_EXTENSION,
        ext_to_mime_map: dict[str, str] = EXTENSION_TO_MIME,
    ):
        """Usable fields are: extension, bytesio, mime_type"""
        if extension is None and mime_type is None:
            raise ValueError("Either extension or mime_type must be provided")

        if extension is not None:
            self.extension = extension
            self.mime_type = ext_to_mime_map[extension]
        else:
            self.mime_type = mime_type
            self.extension = mime_to_ext_map[mime_type]

        if isinstance(bytes_or_bytesio, bytes_or_bytesio):
            self.bytesio = BytesIO(bytes_or_bytesio)
        elif isinstance(bytes_or_bytesio, BytesIO):
            self.bytesio = bytes_or_bytesio

    @property
    def filename(self) -> str:
        """Return random filename of letters and numbers
        with a length of 8 characters with extension"""
        return (
            "".join(random.choices(string.ascii_letters + string.digits, k=8))
            + f".{self.extension}"
        )
