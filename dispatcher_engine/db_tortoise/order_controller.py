import secrets
from datetime import datetime

from fastapi import UploadFile

import config
from db_tortoise.helper_enums import OrderRequestType
from db_tortoise.orders_models import Order


class OrderController:
    @classmethod
    async def advance_order_stage(cls, order: Order) -> None:
        # assign filenames if missing
        if not order.current_stage:
            await cls._assign_filenames(order)
            order.status = "active"

        if order.current_stage == "ready_for_send":
            order.current_stage = "sending"
            return

        if order.current_stage == "sending":
            order.status = "completed"
            order.current_stage = "finished"
            return

        # report error in case of error
        if order.error:
            order.current_stage = "ready_for_send"
            return

        # advance according to the request_type
        match order.request_type:
            case OrderRequestType.VIDEO_AUTO:
                return await cls._advance_video_auto(order)
            case OrderRequestType.VIDEO_FILES:
                return await cls._advance_video_files(order)
            case OrderRequestType.ONLY_SCREENSHOTS:
                return await cls._advance_only_screenshots(order)
            case _:
                return None

    @classmethod
    async def _generate_filenames(cls):
        background_name = f"01_BG_{secrets.token_hex(8)}.png"
        foreground_name = f"02_FG_{secrets.token_hex(8)}.png"
        video_gfx_name = f"video-gfx-{secrets.token_hex(8)}.mp4"
        html_assembly_name = f"gfx_html_{datetime.now().strftime('%Y%m%d_%H-%M-%S_%f')}"
        return background_name, foreground_name, video_gfx_name, html_assembly_name

    @classmethod
    async def _assign_filenames(cls, order: Order):
        (
            background_name,
            foreground_name,
            video_gfx_name,
            html_assembly_name,
        ) = await cls._generate_filenames()
        match order.request_type:
            case OrderRequestType.VIDEO_AUTO:
                order.background_name = background_name
                order.foreground_name = foreground_name
                order.video_gfx_name = video_gfx_name
                order.html_assembly_name = html_assembly_name
            case OrderRequestType.VIDEO_FILES:
                order.video_gfx_name = video_gfx_name
                order.html_assembly_name = html_assembly_name
                if order.background_screenshot:
                    order.background_name = background_name
            case OrderRequestType.ONLY_SCREENSHOTS:
                order.background_name = background_name
                order.foreground_name = foreground_name
            case _:
                return

    @classmethod
    async def _advance_video_auto(cls, order: Order) -> None:
        match order.current_stage:
            case "ready_for_screenshots":
                next_stage = "screenshots_pending"

            case "screenshots_pending":
                next_stage = "ready_for_video_gfx"

            case "ready_for_video_gfx":
                next_stage = "video_gfx_pending"

            case "video_gfx_pending":
                next_stage = "ready_for_send"

            case "ready_for_send":
                next_stage = "sending"

            case _:
                # in case of new order
                next_stage = "ready_for_screenshots"

        order.current_stage = next_stage

    @classmethod
    async def _advance_video_files(cls, order: Order) -> None:
        match order.current_stage:
            case "ready_for_screenshots":
                next_stage = "screenshots_pending"

            case "screenshots_pending":
                next_stage = "ready_for_video_gfx"

            case "ready_for_video_gfx":
                next_stage = "video_gfx_pending"

            case "video_gfx_pending":
                next_stage = "ready_for_send"

            case "ready_for_send":
                next_stage = "sending"

            case _:
                # in case of new order
                # check if background screendshot needed as the background image
                if order.background_screenshot:
                    next_stage = "ready_for_screenshots"
                else:
                    next_stage = "ready_for_video_gfx"

        order.current_stage = next_stage

    @classmethod
    async def _advance_only_screenshots(cls, order: Order) -> None:
        match order.current_stage:
            case "ready_for_screenshots":
                next_stage = "screenshots_pending"
            case "screenshots_pending":
                next_stage = "ready_for_send"
            case "ready_for_send":
                next_stage = "sending"
            case _:
                # in case of new order
                next_stage = "ready_for_screenshots"

        order.current_stage = next_stage

    @classmethod
    async def save_user_files(cls, order: Order) -> None:
        # handle file saves
        if getattr(order, "audio_file", None):
            audio_name = await cls._save_user_file(order.audio_file)
            order.audio_name = audio_name
        if getattr(order, "foreground_file", None):
            foreground_name = await cls._save_user_file(order.foreground_file)
            order.foreground_name = foreground_name
        if getattr(order, "background_file", None):
            background_name = await cls._save_user_file(order.background_file)
            order.background_name = background_name
        return

    @classmethod
    async def _save_user_file(cls, file: UploadFile = None) -> str:
        """Save a UploadFile instance to VOLUME and return new filename"""
        temp_name = f"user_{secrets.token_hex(8)}"
        extension = file.filename.split(".")[-1]
        full_filename = f"{temp_name}.{extension}"
        save_path = config.USER_FILES_FOLDER / full_filename
        with open(save_path, "wb+") as output_file:
            output_file.write(file.file.read())
        return full_filename
