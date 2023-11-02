import traceback
from time import perf_counter

import config

from video_gfx.animation_configurator import create_animation_parameters
from video_gfx.create_html_gfx import create_html
from video_gfx.get_storage import get_order_files_from_storage_unit
from video_gfx.png_extractor import extract_png_sequence
from video_gfx.png_stitcher import stitch_images


def create_video_gfx(order: dict) -> bool:
    """Creates a video of multiple files like Background and Foreground images,
    adds audio file if neccessary and returns path to a ready video"""
    # create animation parameters object
    try:
        print("getting files from storage", flush=True)
        # get files from storage unit
        get_order_files_from_storage_unit(order)

        print("creating animation parameters", flush=True)
        # weird too complicated function...
        animation_parameters = create_animation_parameters(order)

        print("building html", flush=True)
        # build html page with animation
        html_assembly_name: str = order.get("html_assembly_name")
        html_assembly_path = config.HTML_ASSEMBLIES_FOLDER / html_assembly_name

        create_html(animation_parameters.to_object(), str(html_assembly_path))

        print("extracting pngs", flush=True)
        # extract pngs
        t1 = perf_counter()
        extract_png_sequence(str(html_assembly_name))
        t2 = perf_counter()
        print("png extraction took", t2 - t1, flush=True)

        print("stitching pngs", flush=True)
        # stitch pngs to mp4
        t1 = perf_counter()
        png_path = html_assembly_path / "png_sequence"
        ready_video_path = config.RENDER_OUTPUT_PATH / order["video_gfx_name"]
        audio_path = (
            animation_parameters.audio_path
            if animation_parameters.audio_enabled
            else ""
        )
        stitch_images(str(png_path), str(ready_video_path), audio_path)
        t2 = perf_counter()
        print("stitching pngs took", t2 - t1, flush=True)
        return True, None
    except Exception as e:
        print(e, flush=True)
        print(str(e), flush=True)
        traceback.print_exception(e)
        return False, str(e)
