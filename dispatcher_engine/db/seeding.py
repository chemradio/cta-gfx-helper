seed_orders = [
    {
        "user_email": "chemradio@gmail.com",
        "status": "error",
        "error": True,
        "error_type": "screenshots",
        "request_type": "video_auto",
        "link": "https://meduza.io/feature/2023/02/19/na-berlinale-2023-pokazali-manodrom-psihologicheskiy-triller-s-dzhessi-ayzenbergom",
        "quote_enabled": True,
        "quote_text": "Южноафриканский режиссер Джон Тренгов продолжает исследовать тему подавленных мужских желаний, которые приводят к всплеску насилия и безумия. Об этом и его первая англоязычная картина — «Манодром», которую показали на Берлинале-2023.",
        "quote_author_enabled": True,
        "quote_author_text": "MEDUZA",
        "stage": "results_confirmed",
        "audio_enabled": False,
    },
    {
        "user_email": "chemradio@gmail.com",
        "status": "error",
        "error": True,
        "error_type": "screenshots",
        "request_type": "video_auto",
        "link": "https://meduza.io/feature/2023/02/17/kak-proverit-zavedeno-li-protiv-menya-v-rf-delo-za-feyki-diskreditatsiyu-pomosch-nezhelatelnoy-organizatsii-ili-za-chto-nibud-esche",
        "quote_enabled": True,
        "quote_text": "Кинематограф переживает времена, когда ярчайшими звездами становятся женщины: персонажи, актрисы, постановщицы. В жюри Берлинале-2023, возглавляемом голливудской звездой Кристен Стюарт, на пять женщин приходится двое мужчин.",
        "quote_author_enabled": True,
        "quote_author_text": "Антон Долин, кинокритик",
        "stage": "results_confirmed",
        "audio_enabled": False,
    },
    {
        "telegram_id": 123797835,
        "status": "processing",
        "request_type": "video_auto",
        "link": "https://meduza.io/",
        "quote_enabled": False,
        "stage": "screenshots",
        "audio_enabled": False,
    },
]


# user_email
# telegram_id


def seed_db():
    from db.sql_handler import db

    db.recreate_tables()
    db.init_add_admin()

    for order in seed_orders:
        db.add_order(**order)


if __name__ == "__main__":
    seed_db()
