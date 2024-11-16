from io import BytesIO
from pathlib import Path
import sys
import subprocess
import re
import secrets
from . import convert_pdf_to_png


async def convert_word_to_png(file_bytesio: BytesIO) -> BytesIO:
    random_filename = {secrets.token_hex(8)}
    docx_path = Path.cwd() / f"{random_filename}.docx"
    pdf_path = Path.cwd() / f"{random_filename}.pdf"

    with open(docx_path, "wb") as f:
        f.write(file_bytesio.getvalue())

    # convert word to pdf
    await convert_word_to_pdf(
        str(Path.cwd().absolute()),
        str(docx_path.absolute()),
    )
    docx_path.unlink()

    with open(pdf_path, "rb") as f:
        pdf_bytesio = BytesIO(f.read())
    pdf_path.unlink()

    # convert pdf to png
    return await convert_pdf_to_png(pdf_bytesio)


async def convert_word_to_pdf(output_folder: str, source_file_path: str, timeout=None):
    def libreoffice_exec():
        if sys.platform == "darwin":
            return "/Applications/LibreOffice.app/Contents/MacOS/soffice"
        return "libreoffice"

    args = [
        libreoffice_exec(),
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        output_folder,
        source_file_path,
    ]

    process = subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout
    )
    filename = re.search("-> (.*?) using filter", process.stdout.decode())

    if filename is None:
        raise Exception(process.stdout.decode())
    else:
        return filename.group(1)
