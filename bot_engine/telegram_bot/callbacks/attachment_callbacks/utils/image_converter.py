from PIL import Image

from telegram_bot.callbacks.attachment_callbacks.attachment_exceptions import (
    FailedConvertImage,
)


async def convert_image_file(file_path) -> bool:
    if not str(file_path).lower().endswith(".png"):
        save_path = f"{file_path}.png"
    else:
        save_path = file_path

    try:
        # convert photo for better optimization / performance or fixing errors
        with Image.open(file_path) as image:
            image.save(save_path, "PNG")
        return save_path

    except Exception as e:
        raise FailedConvertImage(e)
