from processors.filename_generator import assign_filenames


def process_order(order: dict) -> dict:
    request_type = order.get("request_type")
    if not order.get("current_stage"):
        order = assign_filenames(order)
        order["status"] = "active"

    match request_type:
        case "video_auto":
            return process_video_auto(order)
        case "video_files":
            return process_video_files(order)
        case "only_screenshots":
            return process_only_screenshots(order)
        case _:
            return None


def process_video_auto(order) -> dict:
    current_stage = order.get("current_stage")
    match current_stage:
        case "screenshots_pending":
            if order.get("screenshots_ready"):
                current_stage = "video_gfx_pending"
        case "video_gfx_pending":
            if order.get("video_gfx_ready"):
                current_stage = "ready_to_send"
        case _:
            # in case of new order
            current_stage = "screenshots_pending"

    order.update({"current_stage": current_stage})
    return order


def process_video_files(order) -> dict:
    current_stage = order.get("current_stage")
    match current_stage:
        case "video_gfx_pending":
            if order.get("video_gfx_ready"):
                current_stage = "ready_to_send"
        case _:
            # in case of new order
            current_stage = "video_gfx_pending"

    order.update({"current_stage": current_stage})
    return order


def process_only_screenshots(order) -> dict:
    current_stage = order.get("current_stage")
    match current_stage:
        case "screenshots_pending":
            if order.get("screenshots_ready"):
                current_stage = "ready_to_send"
        case _:
            # in case of new order
            current_stage = "screenshots_pending"

    order.update({"current_stage": current_stage})
    return order
