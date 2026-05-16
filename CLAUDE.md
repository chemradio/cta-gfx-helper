# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Telegram bot that produces graphics for media/news content: web-page screenshots, "video graphics"
(quote/animation videos), and read-time estimates. The user-facing bot interface and messages are in
Russian. The system runs as a set of Docker containers orchestrated by `compose_containers/docker-compose.yml`.

## Running

```bash
./run.sh        # copies the shared lib into each container, then `docker compose up --build`
```

`run.sh` first calls `scripts/copy_libs.sh`, then runs `docker compose down && up --build` from
`compose_containers/`. Build platform is `linux/arm64`.

Required environment variables (see `env_variables.txt`): `REGISTER_PASSPHRASE`, `BOT_ADMIN_PASSWORD`,
`BOT_ADMIN_EMAIL`, `POSTGRES_PASSWORD`, `JWT_SECRET`, `VERTICAL_RESOLUTION`, `HORIZONTAL_RESOLUTION`,
`FONT_SMOOTHING`, plus `BOT_TOKEN` and `BOT_ADMIN` referenced by docker-compose. A `cookie_file.json`
must be pushed to the bot (via the `/cookie_file` command) so the screenshot/video engines can
authenticate to social networks.

## The shared library: `py_gfxhelper_lib`

`libs/py_gfxhelper_lib/` is the **single source of truth** for shared code (`QueueManager`, `DBHandler`,
`AssetFile`, FastAPI routers, order/user enums, intercontainer request helpers, readtime calc).

`scripts/copy_libs.sh` copies `libs/` into every `compose_containers/*/libs/` directory **and** into
`tests/libs/`, replacing whatever is there. The per-container `libs/` copies are build artifacts —
**edit `libs/py_gfxhelper_lib/` only**, never the copies. `run.sh` re-syncs them on every run.

## Architecture

Containers (each a separate folder under `compose_containers/`, each its own Dockerfile/requirements):

- **db** — MongoDB 6.0, data persisted to `compose_containers/mongodata/`.
- **dispatcher** (`dispatcher_engine`, FastAPI :9000) — the orchestrator. Owns the Mongo database
  (users, orders), authentication (JWT), and the order pipeline.
- **bot-engine** (`bot_engine`) — the Telegram bot (python-telegram-bot, long-polling). Pure UI layer:
  collects an order through callback flows, then POSTs it to the dispatcher.
- **file_converter** (`file_converter`, FastAPI :9005) — converts unsupported files (LibreOffice,
  ffmpeg) and rescales images.
- **screenshoter** (`screenshot_engine`, FastAPI :9002) — captures web screenshots via Selenium.
- **video-gfx** (`video_gfx`, FastAPI :9004) — renders video graphics via Selenium + ffmpeg.
- **screenshot-selenium / video-gfx-selenium-1..3** — remote Selenium browser nodes used by the two
  engines above.

Order flow: bot collects input → POSTs to dispatcher → `order_processor/order_processor.py` matches on
`OrderRequestType` (`readtime`, `only_screenshots`, `video_auto`, `video_files`, `video_mixed`) and runs
the matching `request_processors/*` → those call out to the `screenshoter` / `video-gfx` /
`file_converter` containers via `order_processor/container_processors/` → results are sent back to the
user through `order_processor/user_reporter/` (Telegram API). Containers reach each other by Docker
hostname (e.g. `http://dispatcher:9000`, see each container's `config.py`).

Long-running work inside the screenshot and video engines is handled by `QueueManager` (a background
thread draining a `deque`); job state is tracked in a TinyDB JSON file (`DBHandler`), and progress is
polled via the shared `order_check`/`file_server` FastAPI routers.

## Tests

`tests/` contains **integration scripts**, not a pytest suite — they hit already-running containers
over HTTP with `httpx`. Run a scenario by executing the script directly, e.g.:

```bash
python tests/container_tests/screenshot_tests.py
```

`tests/requirements.txt` installs `httpx` and the local `py_gfxhelper_lib`. `tests/libs/` is a
copy_libs.sh artifact; `tests/screenshot_links.json` holds sample input URLs.
