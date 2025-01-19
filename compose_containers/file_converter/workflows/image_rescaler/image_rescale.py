from py_gfxhelper_lib.files.asset_file import AssetFile
from PIL import Image
import io


async def image_rescale(
     max_width: int | float | None, max_height: int | float | None
) -> AssetFile:
    if not max_width and not max_height:
        raise ValueError("At least one of max_width or max_height must be provided")
    # Open the image file
    image = 

    image_aspect_ratio = image.width / image.height
    if max_width and max_height:
        target_aspect_ratio = max_width / max_height
        if image_aspect_ratio > target_aspect_ratio:
            new_width = max_width
            new_height = int(max_width / image_aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * image_aspect_ratio)
    elif max_width:
        ...
    # if image.width > max_width or image.height > max_height:
    #     if aspect_ratio > 1:
    #         new_width = min(image.width, max_width)
    #         new_height = int(new_width / aspect_ratio)
    #     else:
    #         new_height = min(image.height, max_height)
    #         new_width = int(new_height * aspect_ratio)
    # else:
    #     new_width, new_height = image.width, image.height

    # # Resize the image
    # resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

    # # Save the resized image back to the AssetFile
    # output = io.BytesIO()
    # resized_image.save(output, format=image.format)
    # return AssetFile(bytes_or_bytesio=output, extension=image_file.extension)
    ...



def rescale_image(image_file: AssetFile, max_width:int|float|None=None, max_height:int|float|None=None):
    with Image.open(image_file.bytesio) as original_image:
        original_width, original_height = img.size
        output_bytesio = io.BytesIO()
        
        # Check if resizing is necessary
        if max_width and max_height:
            if max_width >= original_width and max_height >= original_height:
                img.save(output_bytesio, format=original_image.format)
                return
            img.thumbnail((max_width, max_height))
        elif max_width:
            if max_width >= original_width:
                img.save(output_bytesio, format=original_image.format)
                return
            scale_factor = max_width / original_width
            new_height = int(original_height * scale_factor)
            img = img.resize((max_width, new_height), Image.ANTIALIAS)
        elif max_height:
            if max_height >= original_height:
                img.save(output_bytesio, format=original_image.format)
                return
            scale_factor = max_height / original_height
            new_width = int(original_width * scale_factor)
            img = img.resize((new_width, max_height), Image.ANTIALIAS)
        
        img.save(output_path)