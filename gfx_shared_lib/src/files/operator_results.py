from dataclasses import dataclass, field
from .asset_file import AssetFile


@dataclass
class OperatorResults:
    success: bool
    operator_output: list[AssetFile] | None = field(default_factory=list)
    error: bool = False
    error_message: str | None = None
