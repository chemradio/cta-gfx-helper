from py_gfxhelper_lib.files.asset_file import AssetFile
import PIL
import io

PIL.Image.MAX_IMAGE_PIXELS = None


async def rescale_image(
    image_file: AssetFile,
    max_width: int | float | None = None,
    max_height: int | float | None = None,
) -> AssetFile:
    if not max_width and not max_height:
        raise ValueError("At least one of max_width or max_height must be provided")

    with PIL.Image.open(image_file.bytesio) as original_image:
        original_width, original_height = original_image.size
        if not max_width:
            max_width = original_width

        if not max_height:
            max_height = original_height

        original_image.thumbnail((max_width, max_height))

        output_bytesio = io.BytesIO()
        original_image.save(output_bytesio, format="PNG")

        return AssetFile(
            bytes_or_bytesio=output_bytesio,
            extension="png",
        )
