import traceback


from py_gfxhelper_lib.custom_types import OperatorResults
from py_gfxhelper_lib.files import AssetFile
from .videogfx_processor.videogfx_studio import create_videogfx


def main_videogfx(
    order: dict,
    remote_driver_url_list: list[str],
) -> OperatorResults:
    success = False
    error = False
    error_message = ""
    operator_output: list[AssetFile] = list()

    try:
        videogfx_bytesio = create_videogfx(
            order,
            remote_driver_url_list,
        )
        success = True

    except Exception as e:
        success = False
        error = True
        error_message = str(e)
        print(f"{error_message=}", flush=True)
        full_traceback = traceback.format_exc()
        print(full_traceback, flush=True)

    if success:
        operator_output.append(
            AssetFile(bytes_or_bytesio=videogfx_bytesio, extension="mp4")
        )
    else:
        print(f"VideoGFX failed.")

    return OperatorResults(
        success=success,
        operator_output=operator_output,
        error=error,
        error_message=error_message,
    )
