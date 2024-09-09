from io import BytesIO
from pathlib import Path

from src.frame_extractor import extract_frame_images
from src.helpers import remove_tree
from src.html_composer import compose_html


def create_videogfx(
    order: dict,
    remote_driver_url_list: list[str],
) -> BytesIO:
    html_path = compose_html(order=order)

    frames_path = extract_frame_images(
        html_path, remote_driver_url_list, order["framerate"]
    )

    ready_videogfx_path: Path = stitch_frames(frames_path, order["framerate"])

    with open(ready_videogfx_path, "rb") as f:
        content = BytesIO(f.read())

    # cleanup
    remove_tree(frames_path)
    remove_tree(html_path)
    remove_tree(ready_videogfx_path)

    return content
