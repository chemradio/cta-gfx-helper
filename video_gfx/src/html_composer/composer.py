import datetime
import json
import os
import shutil
from pathlib import Path

import pydub
from fastapi import UploadFile


def compose_html(
    order: dict,
    storage_path: Path = Path.cwd() / "temp",
    audio_offset: float = 0.3,
    default_animation_duration: int | float = 25,
) -> Path:
    # copy template files
    template_name = order.get("videogfx_template", "ct_main")
    template_path = __file__.storage_path / "html_templates" / template_name

    if not template_path.exists():
        raise Exception(f"Template not found: {template_name}")

    html_assembly_path = (
        storage_path
        / f"ha_{template_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    )
    shutil.copytree(template_path, html_assembly_path)

    # extract files from dict
    files_to_extract = ("background_file", "foreground_file", "audio_file")
    for file in files_to_extract:
        dict_file = order.get(file)
        if not dict_file:
            continue
        with open(html_assembly_path / dict_file.filename, "wb") as f:
            f.write(dict_file.file.read())

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
        "animationDuration": default_animation_duration,
    }

    # get audio file duration
    audio_file = order.get("audio_file")
    if audio_file:
        audio = pydub.AudioSegment.from_file(audio_file.file)
        audio_duration = audio.duration_seconds
        parameters["animationDuration"] = audio_duration + audio_offset

    # Overrides are template specific instructions to a template.
    # These override default template animation settings
    # for certain elements like text, images, etc.
    # To be implemented in the future.
    overrides = {}
    parameters.update(overrides)

    config_json_path = os.path.join(html_assembly_path, "config.json")
    with open(config_json_path, "w+") as config_file:
        json.dump(parameters, config_file)

    return html_assembly_path
