from processors.filename_generator import assign_filenames


def advance_order_stage(order: dict) -> dict:
    request_type = order.get("request_type")
    current_stage = order.get("current_stage")

    # assign filenames if missing
    if not current_stage:
        order = assign_filenames(order)
        order["status"] = "active"

    if current_stage == "ready_for_send":
        order["current_stage"] = "sending"
        return order

    if current_stage == "sending":
        order["status"] = "completed"
        order["current_stage"] = "finished"
        return order

    # report error in case of error
    if order.get("error"):
        order["current_stage"] = "ready_for_send"
        return order

    match request_type:
        case "video_auto":
            return advance_video_auto(order)
        case "video_files":
            return advance_video_files(order)
        case "only_screenshots":
            return advance_only_screenshots(order)
        case _:
            return None


def advance_video_auto(order) -> dict:
    current_stage = order.get("current_stage")
    match current_stage:
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

    order.update({"current_stage": next_stage})
    return order


def advance_video_files(order) -> dict:
    current_stage = order.get("current_stage")
    match current_stage:
        case "ready_for_video_gfx":
            next_stage = "video_gfx_pending"

        case "video_gfx_pending":
            next_stage = "ready_for_send"

        case "ready_for_send":
            next_stage = "sending"

        case _:
            # in case of new order
            next_stage = "ready_for_video_gfx"

    order.update({"current_stage": next_stage})
    return order


def advance_only_screenshots(order) -> dict:
    current_stage = order.get("current_stage")
    match current_stage:
        case "ready_for_screenshots":
            next_stage = "screenshots_pending"
        case "screenshots_pending":
            next_stage = "ready_for_send"
        case "ready_for_send":
            next_stage = "sending"
        case _:
            # in case of new order
            next_stage = "ready_for_screenshots"

    order.update({"current_stage": next_stage})
    return order
