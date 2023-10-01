import traceback

import config

from video_gfx.animation_configurator import create_animation_parameters
from video_gfx.create_html_gfx import create_html
from video_gfx.direct_recording.direct_recorder import record_gfx
from video_gfx.get_storage import get_order_files_from_storage_unit


def create_video_gfx(order: dict) -> bool:
    """Creates a video of multiple files like Background and Foreground images,
    adds audio file if neccessary and returns path to a ready video"""
    # create animation parameters object
    try:
        print("getting files from storage", flush=True)
        # get files from storage unit
        get_order_files_from_storage_unit(order)

        print("creating animation parameters", flush=True)
        animation_parameters = create_animation_parameters(order)

        print("building html", flush=True)
        html_assembly_name: str = order.get("html_assembly_name")
        html_assembly_path = config.HTML_ASSEMBLIES_FOLDER / html_assembly_name
        create_html(animation_parameters.to_object(), str(html_assembly_path))

        print("recording xvfb", flush=True)
        record_gfx(
            html_assembly_name,
            config.RENDER_OUTPUT_PATH / order["video_gfx_name"],
            animation_parameters.audio_path
            if animation_parameters.audio_enabled
            else "",
        )

        return True, None
    except Exception as e:
        print(e, flush=True)
        print(str(e), flush=True)
        traceback.print_exception(e)
        return False, str(e)
