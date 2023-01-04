#! /bin/sh
python3 cleanup_dev_folder.py

docker compose down -v

docker compose up --build