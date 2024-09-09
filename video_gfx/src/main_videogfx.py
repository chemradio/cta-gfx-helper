from pathlib import Path

from shared import FilenameType, OperatorOutputFile, OperatorResults, generate_filename

from .videogfx_processor.videogfx_studio import create_videogfx


def main_videogfx(
    order: dict,
    remote_driver_url_list: list[str],
) -> OperatorResults:
    success = False
    error = False
    error_message = ""
    operator_output: list[OperatorOutputFile] = list()

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

    if success:
        operator_output.append(
            OperatorOutputFile(
                content=videogfx_bytesio,
                filename=generate_filename(FilenameType.VIDEOGFX_VIDEO),
            )
        )
    else:
        print(f"VideoGFX failed.")

    return OperatorResults(
        success=success,
        operator_output=operator_output,
        error=error,
        error_message=error_message,
    )
