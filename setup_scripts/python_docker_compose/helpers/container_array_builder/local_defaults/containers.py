from local_defaults.config import DefaultConfig
from local_defaults.volumes import local_volume
from templates.container_meta import DockerComposeContainer

dispatcher = DockerComposeContainer(
    name=DefaultConfig.DISPATCHER_NAME,
    build=DefaultConfig.DISPATCHER_BUILD,
    port=DefaultConfig.DISPATCHER_PORT,
    expose=True,
    port_mapping={DefaultConfig.DISPATCHER_PORT: DefaultConfig.DISPATCHER_PORT},
    depends_on={DefaultConfig.DB_NAME: {"condition": "service_healthy"}},
    volumes=[local_volume],
)

front_svelte = DockerComposeContainer(
    name=DefaultConfig.FRONT_SVELTE_NAME,
    build=DefaultConfig.FRONT_SVELTE_BUILD,
    port=DefaultConfig.FRONT_SVELTE_PORT,
    expose=True,
    port_mapping={"80": DefaultConfig.FRONT_SVELTE_PORT},
    depends_on=[DefaultConfig.DISPATCHER_NAME],
    volumes=[local_volume],
)

db = DockerComposeContainer(
    name="db",
    healthcheck={
        "test": ["CMD-SHELL", "pg_isready -U postgres"],
        "interval": "5s",
        "timeout": "5s",
        "retries": 5,
    },
)

screenshoter = DockerComposeContainer(
    name=DefaultConfig.SCREENSHOTER_NAME,
    build=DefaultConfig.SCREENSHOTER_BUILD,
    port=DefaultConfig.SCREENSHOTER_PORT,
    depends_on=[DefaultConfig.DISPATCHER_NAME],
)

video_gfx = DockerComposeContainer(
    name=DefaultConfig.VIDEO_GFX_NAME,
    build=DefaultConfig.VIDEO_GFX_BUILD,
    port=DefaultConfig.VIDEO_GFX_PORT,
    depends_on=[DefaultConfig.DISPATCHER_NAME],
)

video_gfx_server = DockerComposeContainer(
    name=DefaultConfig.VIDEO_GFX_SERVER_NAME,
    build=DefaultConfig.VIDEO_GFX_SERVER_BUILD,
    port=DefaultConfig.VIDEO_GFX_SERVER_PORT,
    depends_on=[DefaultConfig.DISPATCHER_NAME],
)

screenshot_selenium = DockerComposeContainer(
    name=DefaultConfig.SCREENSHOT_SELENIUM_NAME,
    image=DefaultConfig.SCREENSHOT_SELENIUM_IMAGE,
    privileged=True,
    shm_size="4g",
    depends_on=[DefaultConfig.DISPATCHER_NAME],
)

video_gfx_selenium = DockerComposeContainer(
    name=DefaultConfig.VIDEO_GFX_SELENIUM_NAME,
    image=DefaultConfig.VIDEO_GFX_SELENIUM_IMAGE,
    privileged=True,
    shm_size="4g",
    depends_on=[DefaultConfig.DISPATCHER_NAME],
)

telegram_bot = DockerComposeContainer(
    name=DefaultConfig.TELEGRAM_BOT_NAME,
    build=DefaultConfig.TELEGRAM_BOT_BUILD,
    volumes=[local_volume],
    port=DefaultConfig.TELEGRAM_BOT_PORT,
    depends_on=[DefaultConfig.DISPATCHER_NAME],
)

sender = DockerComposeContainer(
    name=DefaultConfig.TELEGRAM_SENDER_NAME,
    build=DefaultConfig.TELEGRAM_SENDER_BUILD,
    volumes=[local_volume],
    port=DefaultConfig.TELEGRAM_SENDER_PORT,
    depends_on=[DefaultConfig.DISPATCHER_NAME],
)
