from io import BytesIO
from .mime_extension_mapping import MIME_TO_EXTENSION, EXTENSION_TO_MIME
import random
import string
from .file_type import FileType


class AssetFile:
    def __init__(
        self,
        bytes_or_bytesio: bytes | BytesIO | None = None,
        extension: str | None = None,
        mime_type: str | None = None,
        text: str | None = None,
        file_type: FileType | str | None = None,
        mime_to_ext_map: dict[str, str] = MIME_TO_EXTENSION,
        ext_to_mime_map: dict[str, str] = EXTENSION_TO_MIME,
    ):
        """Usable fields are: extension, bytesio, mime_type"""
        self.file_type = file_type
        self.text = text
        self._unbound_filename = ""
        self.extension = extension if extension else ""

        if bytes_or_bytesio:
            if extension is None and mime_type is None:
                raise ValueError("Either extension or mime_type must be provided")

            if extension is not None:
                self.extension = extension
                self.mime_type = ext_to_mime_map[extension]
            else:
                self.mime_type = mime_type
                self.extension = mime_to_ext_map[mime_type]

            if isinstance(bytes_or_bytesio, bytes):
                self.bytesio = BytesIO(bytes_or_bytesio)
            elif isinstance(bytes_or_bytesio, BytesIO):
                self.bytesio = bytes_or_bytesio

    @property
    def filename(self) -> str:
        if not self._unbound_filename:
            self._unbound_filename = (
                "".join(random.choices(string.ascii_letters + string.digits, k=8))
                + f".{self.extension}"
            )
        return self._unbound_filename
