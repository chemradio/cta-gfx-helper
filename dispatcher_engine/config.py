from pathlib import Path

SQL_SERVER = "temp.sqlite"
SQL_CONNECT_STRING = f"sqlite:///{SQL_SERVER}"
RECENT_ORDERS_INTERVAL_HOURS = 12
VOLUME_MOUNTPOINT = Path.cwd() / "volume"
RENDER_OUTPUT_PATH = VOLUME_MOUNTPOINT / "video_exports"

# database configuration
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "currenttimeasia"
POSTGRES_HOSTNAME = "db"
POSTGRES_PORT = "5432"
POSTGRES_DB = "postgres"
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB}"


# other containers
SCREENSHOTER_HOSTNAME = "screenshoter"
SCREENSHOTER_PORT = 9002

VIDEOGFX_HOSTNAME = "video_gfx"
VIDEOGFX_PORT = 9004

SENDER_HOSTNAME = "sender"
SENDER_PORT = 9007

SCREENSHOTER_ENDPOINT = (
    f"http://{SCREENSHOTER_HOSTNAME}:{SCREENSHOTER_PORT}/start_screenshoting"
)
VIDEOGFX_ENDPOINT = f"http://{VIDEOGFX_HOSTNAME}:{VIDEOGFX_PORT}/start_video_gfx"
SENDER_ENDPOINT = f"http://{SENDER_HOSTNAME}:{SENDER_PORT}/send_orders"
