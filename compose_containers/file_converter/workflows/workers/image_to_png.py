from io import BytesIO
from PIL import Image


async def convert_image_to_png(file_bytesio: BytesIO) -> BytesIO:
    image = Image.open(file_bytesio)
    png_bytesio = BytesIO()
    image.save(png_bytesio, format="PNG")
    png_bytesio.seek(0)
    return png_bytesio
