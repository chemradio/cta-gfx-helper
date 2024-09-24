from io import BytesIO
from pathlib import Path

from src.frame_extractor import extract_frame_images
from src.frames_to_video import stitch_images
from src.helpers import remove_tree
from src.html_composer import compose_html


def create_videogfx(
    order: dict,
    remote_driver_url_list: list[str],
) -> BytesIO:

    print("starting create_videogfx", flush=True)

    print("composing html", flush=True)
    html_path = compose_html(order)
    print(f"html_path: {html_path}", flush=True)

    print("extracting frames", flush=True)
    frames_path = extract_frame_images(
        html_path, remote_driver_url_list, order["framerate"]
    )
    print(f"frames_path: {frames_path}", flush=True)

    ready_videogfx_path = stitch_images(
        image_folder_path=frames_path,
        framerate=order["framerate"],
        audio_file=order.get("audio_file", None),
        audio_delay=order["audio_offset"],
    )

    # with open(ready_videogfx_path, "rb") as f:
    #     content = BytesIO(f.read())

    # # cleanup
    # remove_tree(frames_path)
    # remove_tree(html_path)
    # remove_tree(ready_videogfx_path)

    # return content
