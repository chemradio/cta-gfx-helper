import mimetypes
import secrets


def get_file_extension_from_mime(mime_type):
    # Returns a tuple with file extension and encoding
    file_extension = mimetypes.guess_extension(mime_type)
    return file_extension


def generate_random_filename(prefix: str = "user", extension: str = str()):
    random_name = secrets.token_hex(12)
    extension = extension[1:] if extension.startswith(".") else extension
    return f"{prefix}_{random_name}.{extension}"
