import pypdfium2 as pdfium


async def convert_pdf_to_image(pdf_file_path: str, image_file_path: str) -> None:
    try:
        pdf = pdfium.PdfDocument(str(pdf_file_path))
        renderer = pdf.render_to(
            pdfium.BitmapConv.pil_image,
            page_indices=[
                0,
            ],
            scale=300 / 72,  # 300dpi resolution
        )
        list(renderer)[0].save(image_file_path)
    except Exception as e:
        print(e)
