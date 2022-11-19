# Telegram bot for TV GFX-elements automation

## Description

This bot serves as an API to Adobe After Effects script to automatically create TV broadcast-ready graphic elements.

It also includes website screenshoting engine to automatically capture images of the websites for consequent incorporating them in gfx-elements.

Bot acts as a replacement for a separate graphics-artist when it comes to basic graphic elements, such as quotes from social media or basic web-page scrolls.

## Instructions

**config_and_db** folder contains admin files that need to be supplied. Basic placeholder for config_template.json is already provided and to be populated by bot admin and renamed to config.json.

**db** files will be automatically generated on first run. To preserve a database of current allowed users and submitted orders - backup **db_allowed_users.json** and **db_orders.json**.

All python requirements are in *requirements.txt*.
