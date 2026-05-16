from io import BytesIO
from pathlib import Path

import config

from src.frame_extractor import extract_frame_images
from src.frame_extractor.playwright_capture import capture_segments
from src.frames_to_video import stitch_images
from src.frames_to_video.segment_stitcher import concat_segments
from src.helpers import remove_tree
from src.html_composer import compose_videogfx


def _render_selenium(
    order: dict,
    html_path: Path,
    remote_driver_url_list: list[str],
    assembly_server_url: str,
) -> Path:
    """Legacy backend: remote Selenium nodes -> PNG sequence on disk -> ffmpeg."""
    frames_path = extract_frame_images(
        html_path, remote_driver_url_list, order["framerate"], assembly_server_url
    )
    return stitch_images(
        image_folder_path=frames_path,
        framerate=order["framerate"],
        audio_file=order.get("audio_file", None),
        audio_delay=order["audio_offset"],
    )


def _render_playwright(
    order: dict,
    html_path: Path,
    assembly_server_url: str,
) -> Path:
    """Playwright backend: headless Chromium -> image2pipe -> parallel segment
    encode -> ffmpeg concat. No PNG sequence touches disk."""
    print(
        f"[playwright] render start | assembly={html_path.name} "
        f"workers={config.SEGMENT_WORKERS} framerate={order['framerate']} "
        f"assembly_server_url={assembly_server_url}",
        flush=True,
    )
    segment_paths = capture_segments(
        html_path,
        order["framerate"],
        assembly_server_url,
        config.SEGMENT_WORKERS,
    )
    return concat_segments(
        segment_paths=segment_paths,
        audio_file=order.get("audio_file", None),
        output_path=html_path / "output.mp4",
        audio_delay=order["audio_offset"],
    )


def create_videogfx(
    order: dict,
    remote_driver_url_list: list[str],
    assembly_server_url: str,
    reduce_images: bool,
) -> BytesIO:
    html_path = compose_videogfx(order, reduce_images=reduce_images)

    if config.FRAME_CAPTURE_BACKEND == "playwright":
        ready_videogfx_path = _render_playwright(order, html_path, assembly_server_url)
    else:
        ready_videogfx_path = _render_selenium(
            order, html_path, remote_driver_url_list, assembly_server_url
        )

    with open(ready_videogfx_path, "rb") as f:
        content = BytesIO(f.read())

    # remove_tree clears the assembly folder's contents (PNG sequence /
    # segments / output video all live under html_path)
    remove_tree(html_path)

    return content
