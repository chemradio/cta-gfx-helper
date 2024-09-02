from io import BytesIO
from pathlib import Path

from src.helpers import remove_tree
from src.html_composer import compose_html


def create_videogfx(
    order: dict, remote_driver_url_list: list[str], audio_offset: float
) -> BytesIO:
    html_path: Path = compose_html(order, audio_offset=audio_offset)

    frame_path: Path = extract_frames(html_path)

    ready_videogfx_path: Path = stitch_frames(frame_path)

    with open(ready_videogfx_path, "rb") as f:
        content = BytesIO(f.read())

    # cleanup
    remove_tree(frame_path)
    remove_tree(html_path)
    remove_tree(ready_videogfx_path)

    return content
