from animation_class_enums import BGAnimation, FGAnimation, AnimationParameters


def create_animation_parameters(order):
    bg_path = order.get('bg_path', '')
    fg_path = order.get('fg_path', '')
    audio_enabled = order.get('audio_enabled', False)
    audio_path = order.get('audio_path', '')
    quote_enabled = order.get('quote_enabled', False)
    quote_text = order.get('quote_text', '')
    quote_author_enabled = order.get('quote_author_enabled', False)
    quote_author = order.get('quote_author', '')
    round_corners = order.get("round_corners_enabled", True)
    single_layer = not order.get('is_two_layer', False)

    request_type = order.get('request_type')

    # manual mode
    if request_type == 'video_files':
        bg_ani_temp = order.get('bg_animation_type', '')
        fg_ani_temp = order.get('fg_animation_type', '')

        # configure manual bg animation
        if not bg_ani_temp:
            bg_animation = BGAnimation.BG_SCROLL
        elif bg_ani_temp == 'scroll':
            bg_animation = BGAnimation.BG_SCROLL
        else:
            bg_animation = BGAnimation.BG_ZOOM

        # configure manual fg animation
        if not fg_ani_temp:
            fg_animation = FGAnimation.ZOOM
        elif fg_ani_temp == 'facebook':
            fg_animation = FGAnimation.FACEBOOK
        elif fg_ani_temp == 'document':
            fg_animation = FGAnimation.DOCUMENT
        elif fg_ani_temp in ('twitter', 'instagram', 'telegram', 'photo'):
            fg_animation = FGAnimation.ZOOM
        else:
            fg_animation = FGAnimation.NONE

    # auto mode
    elif request_type == 'video_auto':
        animation_type = order.get("animation_type")

        if animation_type == 'scroll':
            bg_animation = BGAnimation.BG_ONLY
            single_layer = True
            fg_animation = FGAnimation.NONE
        
        elif animation_type == 'facebook':
            bg_animation = BGAnimation.BG_SCROLL
            fg_animation = FGAnimation.FACEBOOK

        else:
            bg_animation = BGAnimation.BG_SCROLL
            fg_animation = FGAnimation.ZOOM

    print(f"{__name__} {single_layer=}")
    animation_parameters = AnimationParameters(
        bg_animation=bg_animation,
        bg_path=bg_path,
        single_layer=single_layer,
        fg_animation=fg_animation,
        fg_path=fg_path,
        round_corners=round_corners,
        quote_enabled=quote_enabled,
        quote_text=quote_text,
        quote_author_enabled=quote_author_enabled,
        quote_author=quote_author,
        audio_enabled=audio_enabled,
        audio_path=audio_path,
    )
    return animation_parameters






# testing
if __name__ == "__main__":
    order = {
      "status": "success",
      "first_name": "Kamilla",
      "telegram_id": 444069595,
      "chat_id": 444069595,
      "screenshots_ready": True,
      "video_ready": False,
      "start_timestamp": 1655293573.0,
      "request_type": "video_auto",
      "stage": "completed",
      "link": "http://www.nlkg.kg/ru/interview/o-smerti-kazakpaeva_-ob-ugrozax-madumarovu_-o-presledovanii-temirova",
      "animation_type": "scroll",
      "quote_enabled": True,
      "quote_text": "\u041e\u0434\u043d\u043e\u0432\u0440\u0435\u043c\u0435\u043d\u043d\u043e \u0441 \u044d\u0442\u0438\u043c, \u0430\u043d\u0430\u043b\u0438\u0437 \u0432\u044b\u0448\u0435\u043e\u0437\u0432\u0443\u0447\u0435\u043d\u043d\u043e\u0433\u043e \u0437\u0430\u044f\u0432\u043b\u0435\u043d\u0438\u044f \u0434\u0430\u0435\u0442 \u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u043e\u043b\u0430\u0433\u0430\u0442\u044c \u043e \u044f\u0432\u043d\u044b\u0445 \u043d\u0430\u043c\u0435\u0440\u0435\u043d\u0438\u044f\u0445 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0433\u043e \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c \u0441\u043a\u043e\u0440\u043e\u043f\u043e\u0441\u0442\u0438\u0436\u043d\u0443\u044e \u043a\u043e\u043d\u0447\u0438\u043d\u0443 \u041a\u0430\u0437\u0430\u043a\u043f\u0430\u0435\u0432\u0430 \u0432 \u0441\u0432\u043e\u0438\u0445 \u043f\u043e\u043b\u0438\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u0446\u0435\u043b\u044f\u0445. \u0414\u0430\u043d\u043d\u044b\u0435 \u043e\u0431\u0441\u0442\u043e\u044f\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u0430 \u0441\u0432\u0438\u0434\u0435\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u0443\u044e\u0442 \u043e \u043d\u0438\u0437\u043a\u0438\u0445 \u043c\u043e\u0440\u0430\u043b\u044c\u043d\u044b\u0445 \u043e\u0440\u0438\u0435\u043d\u0442\u0438\u0440\u0430\u0445 \u0420\u0430\u0432\u0448\u0430\u043d\u0430 \u0414\u0436\u0435\u0435\u043d\u0431\u0435\u043a\u043e\u0432\u0430, \u043a\u043e\u0442\u043e\u0440\u044b\u0439 \u0440\u0430\u0434\u0438 \u0441\u0432\u043e\u0438\u0445 \u043f\u043e\u043b\u0438\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u0430\u043c\u0431\u0438\u0446\u0438\u0439 \u0433\u043e\u0442\u043e\u0432 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c \u043f\u0430\u043d\u0438\u0445\u0438\u0434\u0443 \u043f\u043e \u0443\u043c\u0435\u0440\u0448\u0435\u043c\u0443 \u0434\u043b\u044f \u0441\u0430\u043c\u043e\u043f\u0438\u0430\u0440\u0430.",
      "quote_author_enabled": True,
      "quote_author": "\u041a\u0430\u043c\u0447\u044b\u0431\u0435\u043a \u0422\u0430\u0448\u0438\u0435\u0432, \u0433\u043b\u0430\u0432\u0430 \u0433\u043e\u0441\u043a\u043e\u043c\u0438\u0442\u0435\u0442\u0430 \u043d\u0430\u0446\u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e\u0441\u0442\u0438 \u041a\u044b\u0440\u0433\u044b\u0437\u0441\u0442\u0430\u043d\u0430",
      "audio_enabled": True,
      "audio_path": "/Users/tim/code/cta-gfx-telegram-bot/assets/user_files//user_ae74b9646e932830.mp3",
      "results_message_id": 17781,
      "render_filename": "Kamilla-gfx-1655293643.mp4",
      "is_two_layer": False,
      "bg_path": "/Users/tim/code/cta-gfx-telegram-bot/assets/screenshots//01_BG_d5cbd92b0e09e12a.png",
      "fg_path": None,
      "link_type": "scroll",
      "start_render_timestamp": 1655293686.598586
    }

    # print(not order.get('is_two_layer', False))
    from pprint import pprint
    pprint(
        create_animation_parameters(order).to_json()

    )