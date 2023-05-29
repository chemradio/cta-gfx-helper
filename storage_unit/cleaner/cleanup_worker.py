import time


def expiry_asset_cleaner() -> None:
    while True:
        print("cleaner working every 30 secs.")
        time.sleep(30)
