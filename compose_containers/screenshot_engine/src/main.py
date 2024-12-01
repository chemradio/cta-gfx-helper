from pathlib import Path


from .screenshot_processor import parse_capture_screenshots
from py_gfxhelper_lib.files import OperatorResults, AssetFile


def main_capture(
    order: dict,
    remote_driver_url: str,
    cookie_file_path: Path,
    dpi_multiplier: int | float,
    attempts: int,
) -> OperatorResults:

    # attempt capture
    url = order["screenshot_link"]
    success = False
    error = False
    error_message = ""
    operator_output = None

    for attempt in range(attempts):
        try:
            capture_results = parse_capture_screenshots(
                url,
                remote_driver_url,
                cookie_file_path,
                dpi_multiplier,
            )
            success = True
            break

        except Exception as e:
            print(f"Attempt: {attempt} Failed to screenshoot url: {url}.", flush=True)
            success = False
            error = True
            error_message = str(e)
            print(f"{error_message=}", flush=True)

    if success:
        operator_output: list[OperatorOutputFile] = list()
        operator_output.append(
            OperatorOutputFile(
                content=capture_results.background.content,
                filename=generate_filename(
                    FilenameType.SCREENSHOT_BACKGROUND,
                ),
            )
        )
        if capture_results.two_layer and capture_results.foreground:
            operator_output.append(
                OperatorOutputFile(
                    content=capture_results.foreground.content,
                    filename=generate_filename(
                        FilenameType.SCREENSHOT_FOREGROUND,
                    ),
                )
            )
    else:
        print(f"Screenshooting failed after {attempts} attempts.")

    return OperatorResults(
        success=success,
        operator_output=operator_output,
        error=error,
        error_message=error_message,
    )
