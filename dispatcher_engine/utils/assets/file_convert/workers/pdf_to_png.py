import secrets
from pathlib import Path

import pypdfium2 as pdfium
from fastapi import UploadFile
from PIL.Image import Image


async def convert_pdf_to_png(file: UploadFile) -> bytes:
    pdf = pdfium.PdfDocument(file.file)
    page = pdf[0]
    bitmap = page.render(
        scale=300 / 72,  # 300dpi resolution
    )
    pil_image: Image = bitmap.to_pil()

    temp_path = Path.cwd() / f"{secrets.token_hex(8)}.png"
    pil_image.save(temp_path, "png")
    with open(temp_path, "rb") as f:
        png_raw = f.read()
    temp_path.unlink()

    return png_raw
