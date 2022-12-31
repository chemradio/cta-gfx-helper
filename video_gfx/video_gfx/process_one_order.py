import config
from video_gfx.animation_configurator import create_animation_parameters
from video_gfx.animation_extractor import extract_png_sequence
from video_gfx.create_html_gfx import create_html
from video_gfx.png_stitcher import stitch_images


def create_video_gfx(order: dict) -> dict:
    """Creates a video of multiple files like Background and Foreground images,
    adds audio file if neccessary and returns path to a ready video"""
    # create animation parameters object
    animation_parameters = create_animation_parameters(order)

    # build html page with animation
    html_assembly_name = create_html(animation_parameters.to_object())
    html_assembly_path = config.HTML_ASSEMBLIES_FOLDER / html_assembly_name

    # extract pngs
    extract_png_sequence(html_assembly_name)

    # stitch pngs to mp4
    png_path = html_assembly_path / "png_sequence"
    ready_video_path = config.RENDER_OUTPUT_PATH / order["video_gfx_name"]
    audio_path = (
        animation_parameters.audio_path if animation_parameters.audio_enabled else ""
    )
    stitch_images(str(png_path), str(ready_video_path), audio_path)

    order.update({"current_stage": "ready_to_send"})
    return order
