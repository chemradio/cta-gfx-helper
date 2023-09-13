from container_interaction.get_file_storage import fetch_file_from_storage


def gather_files_from_storage(order: dict) -> list:
    match order["request_type"]:
        case "video_auto":
            filetypes = ("video_gfx_name",)
        case "video_files":
            filetypes = ("video_gfx_name",)
        case "only_screenshots":
            filetypes = ("background_name", "foreground_name")
        case _:
            return []

    files = list()
    for filetype in filetypes:
        filename = order.get(filetype)
        file_bytes = fetch_file_from_storage(filename)
        if file_bytes:
            files.append((filename, file_bytes))

    return files
