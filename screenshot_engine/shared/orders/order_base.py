from dataclasses import dataclass, field
import uuid
import time
from enum import Enum


class OrderStatus(str, Enum):
    NEW = "NEW"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    FAILED = "FAILED"


@dataclass
class OrderBase:
    order_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created: int = field(default_factory=lambda: int(time.time()))
    output: list[str] = field(default_factory=list)
    status: OrderStatus = OrderStatus.NEW
    error_message: str = ""
    
    def to_dict(self):
        return {
            "order_id": self.order_id,
            "created": self.created,
            "output": self.output,
            "status": self.status,
            "error_message": self.error_message,
        }