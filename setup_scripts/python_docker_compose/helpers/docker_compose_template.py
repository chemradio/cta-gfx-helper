docker_compose_dict = {
    "version": "3.9",
    "services": {
        "dispatcher": {
            "build": "./dispatcher_engine",
            "args": [
                {"REBUILD_DB": True},
            ],
            "volumes": [
                {"asset_storage": "/usr/src/app/volume"},
                {"./dispatcher_engine": "/usr/src/app"},
            ],
            "environment": [{}],
            "expose": ["9000"],
            "ports": ["9000:9000"],
            "depends_on": {"db": {"condition": "service_healthy"}},
        },
        "front_svelte": {
            "build": "./front_svelte",
            "volumes": [
                {
                    "asset_storage": "/usr/src/app/volume",
                },
                {"./front_svelte": "/usr/src/app/"},
            ],
            "expose": ["9009"],
            "ports": {
                {
                    "80:9009",
                },
            },
            "depends_on": ["dispatcher"],
        },
        "db": {
            "image": "postgres:15-alpine",
            # environment:
            #   - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
            "healthcheck": {
                "test": ["CMD-SHELL", "pg_isready -U postgres"],
                "interval": "5s",
                "timeout": "5s",
                "retries": 5,
            },
        },
        "telegram_bot": {
            "build": "./bot_engine",
            "volumes": [
                {
                    "asset_storage": "/usr/src/app/volume",
                },
                {"./bot_engine": "/usr/src/app/"},
            ],
            "expose": [
                "9001",
            ],
            "depends_on": ["dispatcher"],
        },
        "screenshoter": {
            "build": "./screenshot_engine",
            "volumes": [
                {
                    "asset_storage": "/usr/src/app/volume",
                },
                {"./screenshot_engine": "/usr/src/app"},
            ],
            "hostname": "screenshoter",
            "expose": [
                "9002",
            ],
            "depends_on": ["dispatcher"],
        },
        "video_gfx": {
            "build": "./video_gfx",
            "volumes": [
                {
                    "asset_storage": "/usr/src/app/volume",
                },
                {
                    "./video_gfx": "/usr/src/app",
                },
            ],
            "expose": [
                "9002",
            ],
            "depends_on": ["dispatcher"],
        },
        "video_gfx_server": {
            "build": "./video_gfx_server",
            "volumes": [
                {
                    "asset_storage": "/usr/src/app/volume",
                },
            ],
            "expose": ["9006"],
            "depends_on": ["dispatcher"],
        },
        "sender": {
            "build": "./sender_engine",
            "volumes": [
                {
                    "asset_storage": "/usr/src/app/volume",
                },
                {
                    "./sender_engine": "/usr/src/app",
                },
            ],
            "expose": ["9007"],
            "depends_on": ["dispatcher"],
        },
        "screenshot_selenium": {
            # "image": "selenium/standalone-chrome",
            "image": "seleniarm/standalone-chromium",
            "hostname": "screenshot_selenium",
            "privileged": True,
            "shm_size": "4g",
            "depends_on": ["dispatcher"],
        },
        "video_gfx_selenium": {
            # "image": "selenium/standalone-chrome",
            "image": "seleniarm/standalone-chromium",
            "hostname": "video_gfx_selenium",
            "privileged": True,
            "shm_size": "4g",
            "depends_on": ["dispatcher"],
        },
    },
    "volumes": {
        "asset_storage": {
            "driver": "local",
            "driver_opts": {
                "type": "none",
                "o": "bind",
                "device": "$PWD/dev/volume/asset_storage",
            },
        },
        "pg_data": {
            "driver": "local",
            "driver_opts": {
                "type": "none",
                "o": "bind",
                "device": "$PWD/dev/volume/pg_data/data",
            },
        },
    },
}
