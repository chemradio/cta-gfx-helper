def format_video_files_user_data(user_data: dict) -> dict:
    main_file = user_data.pop("main_file")
    match user_data.pop("background_source"):
        case "no_background":
            user_data["background_name"] = main_file
            user_data["background_screenshot"] = False
        case "background_file":
            user_data["foreground_name"] = main_file
            user_data["background_name"] = user_data.pop("background_file")
            user_data["background_screenshot"] = False
        case "background_screenshot":
            user_data["foreground_name"] = main_file
            user_data["background_screenshot"] = True

    return user_data
