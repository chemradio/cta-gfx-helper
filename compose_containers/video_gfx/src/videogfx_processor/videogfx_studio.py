from io import BytesIO

from src.frame_extractor import extract_frame_images
from src.frames_to_video import stitch_images
from src.helpers import remove_tree
from src.html_composer import compose_videogfx


def create_videogfx(
    order: dict,
    remote_driver_url_list: list[str],
    assembly_server_url: str = "http://video_gfx:9004/storage",
) -> BytesIO:
    html_path = compose_videogfx(order)
    frames_path = extract_frame_images(
        html_path, remote_driver_url_list, order["framerate"], assembly_server_url
    )
    ready_videogfx_path = stitch_images(
        image_folder_path=frames_path,
        framerate=order["framerate"],
        audio_file=order.get("audio_file", None),
        audio_delay=order["audio_offset"],
    )

    with open(ready_videogfx_path, "rb") as f:
        content = BytesIO(f.read())

    # cleanup
    remove_tree(frames_path)
    remove_tree(ready_videogfx_path)
    remove_tree(html_path)

    return content
