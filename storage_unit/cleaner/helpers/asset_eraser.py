from utils.assets.asset_finder import find_file


def erase_order_assets(order: dict) -> None:
    potential_assets = (
        "background_name",
        "foreground_name",
        "video_gfx_name",
        "audio_name",
    )
    for asset in potential_assets:
        asset_name: str | None = order.get(asset)
        if not asset_name:
            continue

        asset_paths = find_file(asset_name)
        if not asset_paths:
            continue

        for path in asset_paths:
            path.unlink()
