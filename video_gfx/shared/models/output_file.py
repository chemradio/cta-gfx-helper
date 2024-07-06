from io import BytesIO
from dataclasses import dataclass


@dataclass
class OperatorOutputFile:
    content: BytesIO
    filename: str
