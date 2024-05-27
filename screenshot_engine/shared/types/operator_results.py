from io import BytesIO
from dataclasses import dataclass, field

@dataclass
class OutputFile:
    content: BytesIO
    filename: str

@dataclass
class OperatorResults:
    success: bool
    operator_output: list[OutputFile] = field(default_factory=list)
    error: bool = False
    error_message: str | None= None
