import pydantic


class OrderCheck(pydantic.BaseModel):
    order_id: int
    secret_key: str | None = None


class FileRequest(pydantic.BaseModel):
    filename: str
    secret_key: str | None = None
