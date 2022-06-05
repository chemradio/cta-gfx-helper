import sys
sys.path.append('..')

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
# from database.db import db_handler
# import database.db
from database import db
# from ...handlers import status_utils

# Create your views here.
def status_global(request: HttpRequest) -> JsonResponse:
    data = {
        "system": {
            "version": 1.1,
            "versionByGit": datetime.timestamp(status_utils.get_bot_version_git()),
            "appName": "cta-gfx-telegram-bot",
        }
    }
    return JsonResponse(data)


def status_today_orders(request: HttpRequest) -> JsonResponse:
    today_orders = db_handler.get_today_orders()
    print(today_orders)
    # "todayOrders": [
    data = {}
    return JsonResponse(data)


def status_second(request: HttpRequest) -> JsonResponse:
    #
    # "orders": {
    #     "todayOrderCount": 3,
    #     "activeOrders": [
    #         {
    #             "status": "restart_terminated",
    #             "first_name": "Tim",
    #             "telegram_id": 247066990,
    #             "chat_id": 247066990,
    #             "screenshots_ready": true,
    #             "video_ready": false,
    #             "start_timestamp": 1653388292.0,
    #             "request_type": "video_auto",
    #             "stage": "completed",
    #             "link": "http://branding.currenttime.tv/",
    #             "animation_type": "scroll",
    #             "quote_enabled": false,
    #             "audio_enabled": false,
    #             "results_message_id": 16548,
    #             "render_filename": "Tim-gfx-1653388324.mp4",
    #             "is_two_layer": false,
    #             "bg_path": "/Users/tim/code/cta-gfx-telegram-bot/assets/screenshots//01_BG_eb806a03f30253e2.png",
    #             "fg_path": null,
    #             "link_type": "scroll",
    #             "start_render_timestamp": 1653388387.08346
    #         },

    data = {
        "system": {
            "status": "active",
            # "refreshGlobal": true,
            # "systemTime": 1654197354,
            # "runtimeFromLaunch": 180,
            # "runtimeFromError": 180,
            # "errorCount": 2,
            # "networkErrors": 2,
        },
    }
    return JsonResponse(data)
