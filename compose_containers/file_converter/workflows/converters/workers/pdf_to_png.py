import pypdfium2 as pdfium
from PIL.Image import Image
from io import BytesIO


async def convert_pdf_to_png(file_bytesio: BytesIO) -> BytesIO:
    pdf = pdfium.PdfDocument(file_bytesio.getvalue())

    page = pdf[0]
    bitmap = page.render(
        scale=300 / 72,  # 300dpi resolution
    )
    pil_image: Image = bitmap.to_pil()
    output_bytesio = BytesIO()
    pil_image.save(output_bytesio, format="PNG")
    output_bytesio.seek(0)
    return output_bytesio
