from dataclasses import dataclass

from db_mongo.models.orders import Order
from utils.helper_enums.orders import OrderRequestType


class StageFlows:
    START_STAGES = tuple()
    END_STAGES = ("complete",)
    SCREENSHOT_STAGES = ("ready_for_screenshots", "screenshots_pending")
    VIDEO_GFX_STAGES = ("ready_for_video_gfx", "video_gfx_pending")
    SENDING_STAGES = ("ready_for_send", "sending")

    VIDEO_AUTO_STAGES = (
        *SCREENSHOT_STAGES,
        *VIDEO_GFX_STAGES,
        *SENDING_STAGES,
        *END_STAGES,
    )
    VIDEO_MIXED_STAGES = (
        *SCREENSHOT_STAGES,
        *VIDEO_GFX_STAGES,
        *SENDING_STAGES,
        *END_STAGES,
    )
    VIDEO_FILES_STAGES = (*VIDEO_GFX_STAGES, *SENDING_STAGES, *END_STAGES)
    ONLY_SCREENSHOTS_STAGES = (*SCREENSHOT_STAGES, *SENDING_STAGES, *END_STAGES)

    @classmethod
    def advance_stage(cls, order: Order):
        stageflow = cls._get_stageflow(order.request_type)
        current_stage = order.current_stage
        if not current_stage:
            next_stage_index = 0
        else:
            next_stage_index = stageflow.index(current_stage) + 1

        if next_stage_index >= (len(stageflow) - 1):
            order.current_stage = "complete"
            return

        order.current_stage = stageflow[next_stage_index]

    @classmethod
    def _get_stageflow(cls, request_type: str) -> tuple[str]:
        match request_type:
            case OrderRequestType.VIDEO_AUTO:
                return cls.VIDEO_AUTO_STAGES
            case OrderRequestType.VIDEO_FILES:
                return cls.VIDEO_FILES_STAGES
            case OrderRequestType.VIDEO_MIXED:
                return cls.VIDEO_MIXED_STAGES
            case OrderRequestType.ONLY_SCREENSHOTS:
                return cls.ONLY_SCREENSHOTS_STAGES
