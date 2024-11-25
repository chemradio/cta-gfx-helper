from dataclasses import dataclass, field
from .output_file import OperatorOutputFile


@dataclass
class OperatorResults:
    success: bool
    operator_output: list[OperatorOutputFile] | None = field(default_factory=list)
    error: bool = False
    error_message: str | None = None
