from screenshots.capture_screenshots import capture_screenshots

order = {
    "status": "order_creation",
    "order_start_timestamp": 1667411324,
    "request_type": "video_auto",
    "stage": "results_confirmed",
    "link": "https://twitter.com/chemradio/status/1604581193969721345",
    "results_message": "РЕЗУЛЬТАТЫ:\n\n🍱 Тип заказа:: Только скриншоты\n\n🔗 Ссылка для графики: http://0.0.0.0:9000\n\n",
    "order_creation_end_timestamp": 1667411336,
    "telegram_id": 247066990,
    "audio_enabled": False,
    "quote_enabled": True,
    "quote_text": "For the first time on this channel we're performing a downgrade.. so Linus and Luke can try Intel Arc! For the first time on this channel we're performing a downgrade.. so Linus and Luke can try Intel Arc!",
    "quote_author_enabled": True,
    "quote_author_text": "Arc!",
    "background_name": "010.png",
    "foreground_name": "020.png",
}


def main():
    capture_screenshots(order)


if __name__ == "__main__":
    main()
