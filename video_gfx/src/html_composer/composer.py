import datetime
import json
import os
import shutil
from pathlib import Path

import pydub

from shared.utils.asset_file import AssetFile


def compose_html(
    order: dict,
    storage_path: Path = Path.cwd() / "storage",
) -> Path:
    # copy template files
    template_name = order.get("videogfx_template", "ct_main")
    template_path = Path(__file__).parent / "html_templates" / template_name

    if not template_path.exists():
        raise Exception(f"Template not found: {template_name}")

    html_assembly_path = (
        storage_path
        / f"ha_{template_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    )

    shutil.copytree(template_path, html_assembly_path, dirs_exist_ok=True)

    files_to_extract = ("background_file", "foreground_file", "audio_file")
    for filetype in files_to_extract:
        if filetype not in order:
            continue
        with open(html_assembly_path / order[filetype].filename, "wb") as f:
            f.write(order[filetype].file.read())

    # edit template files
    parameters = {
        "verticalResolution": os.environ.get("VERTICAL_RESOLUTION", 1080),
        "singleLayer": False,
        "backgroundClass": "",
        "backgroundPath": f"./{order.get('background_file').filename}",
        "foregroundClass": "",
        "roundCorners": True,
        "foregroundPath": f"./{order.get('foreground_file').filename}",
        "quoteEnabled": (
            True if order.get("quote_enabled") and order.get("quote_text") else False
        ),
        "quoteTextText": order.get("quote_text"),
        "quoteAuthorText": order.get("quote_author_text"),
        "animationDuration": order["animation_duration"],
    }

    # get audio file duration
    audio_file: AssetFile = order.get("audio_file")
    if audio_file:
        audio_file.file.seek(0)
        audio_segment = pydub.AudioSegment.from_file(
            audio_file.file, format=audio_file.filename.split(".")[-1].upper()
        )
        audio_duration = len(audio_segment) / 1000.0
        parameters["animationDuration"] = (
            audio_duration + order["audio_offset"] + order["videogfx_tail"]
        )

    # Overrides are template specific instructions to a template.
    # These override default template animation settings
    # for certain elements like text, images, etc.
    # To be implemented in the future.
    parameters.update(order.get("overrides", {}))

    config_json_path = os.path.join(html_assembly_path, "config.json")
    with open(config_json_path, "w+") as config_file:
        json.dump(parameters, config_file)

    return html_assembly_path
