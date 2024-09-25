import datetime
import json
import os
import shutil
from pathlib import Path

from .animation_duration_calc import calculate_animation_duration


def compose_videogfx(order: dict, storage_path: Path = Path.cwd() / "storage") -> Path:
    html_assembly_path = prepare_html_template(order, storage_path)
    configure_html_comp(order, html_assembly_path)
    return html_assembly_path


def prepare_html_template(
    order: dict, storage_path: Path = Path.cwd() / "storage"
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

    files_to_extract = ("background_file", "foreground_file")
    for filetype in files_to_extract:
        if filetype not in order:
            continue
        with open(html_assembly_path / order[filetype].filename, "wb") as f:
            f.write(order[filetype].file.read())

    return html_assembly_path


def configure_html_comp(order: dict, html_assembly_path: Path):
    # edit template files
    parameters = {
        "verticalResolution": os.environ.get("VERTICAL_RESOLUTION", 1080),
        "backgroundPath": f"./{order.get('background_file').filename}",
        "foregroundPath": f"./{order.get('foreground_file').filename}",
        "quoteEnabled": (
            True if order.get("quote_enabled") and order.get("quote_text") else False
        ),
        "quoteTextText": order.get("quote_text", ""),
        "quoteAuthorText": order.get("quote_author_text", ""),
        "roundCorners": True,
        "animationDuration": calculate_animation_duration(order),
        #
        # to figure out programmatically
        "singleLayer": False if order.get("foreground_file") else True,
        "backgroundClass": "",
        "foregroundClass": "",
    }

    # Overrides are template specific instructions to a template.
    # These override default template animation settings
    # for certain elements like text, images, etc.
    # To be implemented in the future.
    parameters.update(order.get("overrides", {}))

    with open(html_assembly_path / "config.json", "w+") as config_file:
        json.dump(parameters, config_file)
