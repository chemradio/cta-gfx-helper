from PIL import Image

from telegram_bot.callbacks.attachment_callbacks.attachment_exceptions import (
    FailedConvertImage,
)


async def convert_image_file(file_path) -> str:
    target_extension = "png"

    if not str(file_path).lower().endswith(target_extension):
        save_path = f"{file_path}.{target_extension}"
    else:
        save_path = file_path

    try:
        # convert photo for better optimization / performance or fixing errors
        with Image.open(file_path) as image:
            image.save(save_path, "PNG")
        return target_extension

    except Exception as e:
        raise FailedConvertImage(e)
