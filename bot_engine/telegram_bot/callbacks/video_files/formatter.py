def format_video_files_user_data(user_data: dict) -> dict:
    main_file = user_data.pop("main_file")
    match user_data.pop("background_source"):
        case "no_background":
            user_data["background_name"] = main_file
            user_data["background_screenshot"] = False
            user_data["is_two_layer"] = False
        case "background_file":
            user_data["foreground_name"] = main_file
            user_data["background_name"] = user_data.pop("background_file")
            user_data["background_screenshot"] = False
            user_data["is_two_layer"] = True
        case "background_screenshot":
            user_data["foreground_name"] = main_file
            user_data["background_screenshot"] = True
            user_data["is_two_layer"] = True

    return user_data
