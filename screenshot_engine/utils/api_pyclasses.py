import pydantic


class ScreenshotOrderIn(pydantic.BaseModel):
    screenshot_link: pydantic.networks.AnyHttpUrl
    secret_key: str | None = None


class OrderCheck(pydantic.BaseModel):
    order_id: int
    secret_key: str | None = None


class FileRequest(pydantic.BaseModel):
    filename: str
    secret_key: str | None = None