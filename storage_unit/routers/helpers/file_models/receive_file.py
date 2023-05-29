from fastapi import UploadFile
from pydantic import BaseModel

from routers.helpers.enums.upload_file_category import UploadFileCategory


class IntercontainerUploadFile(BaseModel):
    file: UploadFile
    category: UploadFileCategory

    class Config:
        use_enum_values = True
