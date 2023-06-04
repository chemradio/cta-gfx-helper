from config import SCREENSHOT_FOLDER


def cleanup_order(order: dict) -> None:
    store_asset_list = (
        "background_name",
        "foreground_name",
    )
    search_folders = (SCREENSHOT_FOLDER,)

    # find assets
    for asset in store_asset_list:
        asset_name = order.get(asset)
        for folder in search_folders:
            if (folder / str(asset_name)).exists():
                (folder / asset_name).unlink()
