import time
from tkinter import DISABLED
from engines.screenshots.screenshot_order_processor import process_screenshot_orders
from engines.video_gfx_engines import render_video_orders
from engines.video_gfx_html.html_server import create_server
from enum import Enum, auto
from database.db import db_handler
import random
import secrets

class TestRequestType(Enum):
    VIDEO_AUTO = auto()
    VIDEO_FILES = auto()
    ONLY_SCREENSHOTS = auto()


class TestDomains(Enum):
    ALL = auto()
    FACEBOOK = auto()
    TWITTER = auto()
    INSTAGRAM = auto()
    TELEGRAM = auto()
    SCROLL = auto()


class TestDepth(Enum):
    FULL = auto()
    SMALL = auto()


class TestQuoteEnabled(Enum):
    ENABLED = auto()
    DISABLED = auto()




FB_LINKS = {
    'fb_pages': [
        # 'https://www.facebook.com/POTUS',
        # 'https://www.facebook.com/rferl/',
        'https://www.facebook.com/CurrentTimeAsia',
        'https://www.facebook.com/UltimateGuitar/',
    ],
    'fb_groups': [
        'https://www.facebook.com/groups/1624501471207237/',
        'https://www.facebook.com/groups/phototalks.george.kolotov/',
        'https://www.facebook.com/groups/1229100757105102/'
    ],
    'fb_profiles': [
        'https://www.facebook.com/zoli.farkas.10',
        'https://www.facebook.com/fardin.faiyaz.75',
        'https://www.facebook.com/fredrik.thordendal?comment_id=Y29tbWVudDoxMDE2MDI1ODgyOTA2NDUzM180NTA2Nzc0MTM3NzAwNTE%3D',
    ],

    'fb_group_posts': [
        'https://www.facebook.com/groups/1624501471207237/posts/2792774037713302/?__cft__[0]=AZUuV_7fyUItf64lTFDhMpGMlo0QU5qlOcL8YcbClEXP6eYKjl5NnmyyhDAnDP36l1gOb1MjgvKEIZm15qEpqQDKTznqmsb56R_-GRbLHaKarfgp_r9diC28oKn0HQpHat7NA164ApKqxS3Ss2dQxAJY&__tn__=%2CO%2CP-R',
        'https://www.facebook.com/groups/1229100757105102/posts/6149775635037565/',
        'https://www.facebook.com/groups/phototalks.george.kolotov/posts/2607647109455214/',
    ],
    'fb_profile_posts': [
        'https://www.facebook.com/zoli.farkas.10/posts/5516531085073496?__cft__[0]=AZWjvyZlr77_muwRpCReMx9CFLyth62AdmKGPfVTpKzub4zXqWVBorJ8yZMYV8TQda9595hys2jPG68d4QrVvrPAvUyPdJ3UyAm0jDYxfCf8zp_1PN5FHhGCoKkNHg7vv2zpU-YiHVC1PwHA3KJn0d5dYFK-CIk7D1iokExn2HD14w&__tn__=%2CO%2CP-R',
        'https://www.facebook.com/fardin.faiyaz.75/posts/3931298560428904',
        'https://www.facebook.com/misha.mansoor/posts/10160258829064533',
        'https://www.facebook.com/fredrik.thordendal/posts/10160161361968967',
    ],
    'fb_page_posts': [
        'https://www.facebook.com/UltimateGuitar/posts/10166855940390473?__cft__[0]=AZWjvzPOHTzOTW9FO4NWEk270_5dY7DTnCu7FuA00uug_X_QhNdZJl6Jf1ca7gs77GDO8w15IYd0AfTpTZR3_6UekJf7xEJMFkuhSXr1qsl-3zYTNC_WOIyb2fRgXOrgnHrevDgDqDAW3yIt75FWb2EH4uBwDwbm1euyvqiQKAJpeO7_zo6h18jIXeZHDqouxEs&__tn__=%2CO%2CP-R',
        'https://www.facebook.com/ProgrammersCreateLife/posts/5367103723338462?__cft__[0]=AZVHtAPP9KDiq4fH4hQKbhp2aNLQ5dk8RjZctVWqXXduIUPFdElHNUZlFkK_aLJR1gyA6TfPNfLwBrX0pM3WTM9nAyBqozQNQdAjPqPmHu4YpullL1LFZc5pQSx3Bjw9oZj6sjHj5q1RVBaLzZL0cpTHc16MMnL438WGxhXGFeHn_4iFqUF2Bik2CEclJFF7N70&__tn__=%2CO%2CP-R',
    ],
}

TWI_LINKS = {
    'twi_profiles': [
        'https://twitter.com/mishaperiphery',
        'https://twitter.com/JakePeriphery',
        'https://twitter.com/MarkPeriphery',
        'https://twitter.com/tesseractband',
    ],
    'twi_posts': [
        'https://twitter.com/tesseractband/status/1564341646262681601',
        'https://twitter.com/hardlorepod/status/1565888146025222144',
        'https://twitter.com/bosxe/status/1413678623450611714',
        'https://twitter.com/DerejeWordofa/status/1566266807954165760',
        'https://twitter.com/buitengebieden/status/1566138480757018625',
    ],
}

IG_LINKS = {
    'ig_pages': [
        'https://www.instagram.com/mishaperiphery/',
        'https://www.instagram.com/olaenglund/',
        'https://www.instagram.com/thisismonuments/',
        'https://www.instagram.com/abasiconcepts/',
        'https://www.instagram.com/aaronintervals/',
        'https://www.instagram.com/lacarspotter_/',
    ],
    'ig_posts': [
        'https://www.instagram.com/p/ChufNr8NGnL/',
        'https://www.instagram.com/p/Cg4rVOxlaE2/',
        'https://www.instagram.com/p/CdLf_L7uAkF/',
        'https://www.instagram.com/p/CiDaFTtO7-q/',
        'https://www.instagram.com/p/CiAdnVFoSme/',
        'https://www.instagram.com/p/CiAqBAGMPE4/',
        'https://www.instagram.com/p/CiE11A1uYob/',
        'https://www.instagram.com/p/CiA1PKcOl7j/'
    ],
}

TG_LINKS = {
    'tg_pages': [
        'https://t.me/davaipojowe',
        'https://t.me/pythontelegrambotchannel',
        'https://t.me/conflictzone'
    ],
    'tg_posts': [
        'https://t.me/voynareal/19273',
        'https://t.me/voenacher/15613',
        'https://t.me/meduzasignal/1987',
        'https://t.me/meduzasignal/1988',
        'https://t.me/pythontelegrambotchannel/122',
        'https://t.me/davaipojowe/284',
    ],
}

SOCIAL_LINKS = {
    'facebook': FB_LINKS,
    'twitter': TWI_LINKS,
    'instagram': IG_LINKS,
    'telegram': TG_LINKS
}

SCROLL_LINKS = [
    'https://www.guitarworld.com/news/daredevil-pedals-aces-hybrid-amplifier',
    'https://techcrunch.com/2022/09/03/apple-readies-its-next-iphone-joe-rogan-interviews-zuck-and-twitter-purportedly-pauses-plans-to-compete-with-onlyfans/',
    'https://www.reuters.com/world/europe/ukraine-nuclear-plant-loses-power-line-moscow-makes-europe-sweat-over-gas-2022-09-04/',
    'https://www.hrw.org/news/2022/08/29/epic-pakistan-floods-show-need-climate-action',
    'https://en.tengrinews.kz/fotoarchive/melody-of-tengri-590/',
    'https://24.kg/obschestvo/243799_vse_vozmojno_asel_ushla_izbanka_stala_barista_ateper_stroit_jizn_vturtsii/',
]




QUOTE_TEXT_LONG = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
QUOTE_TEXT_MEDIUM = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.'
QUOTE_TEXT_SHORT = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
QUOTE_AUTHOR = "Lorem ipsum, dolor sit amet"


BASE_ORDER_TEMPLATE = {
    "status": "processing",
    "first_name": "tester",
    "telegram_id": 247066990,
    "chat_id": 247066990,
    "video_ready": False,
    "start_timestamp": time.time(),
    "results_message_id": 22785,
    "bg_path": "",
    "fg_path": "",
    "stage": "screenshots",
    "screenshots_ready": False,
    "video_ready": False,
    "is_two_layer": False,
    "link": "",
    "animation_type": "",
    "start_render_timestamp": 0,
    "quote_enabled": False,
    "quote_text": QUOTE_TEXT_MEDIUM,
    "quote_author_enabled": True,
    "quote_author": QUOTE_AUTHOR,
    "audio_enabled": False,
}


VIDEO_AUTO_TEMPLATE = BASE_ORDER_TEMPLATE.copy()
VIDEO_AUTO_TEMPLATE["request_type"] = "video_auto"

ONLY_SCREENSHOTS_TEMPLATE = BASE_ORDER_TEMPLATE.copy() 
ONLY_SCREENSHOTS_TEMPLATE["request_type"] = "only_screenshots"


def create_test_orders(request_type: TestRequestType, test_domains: TestDomains,
                        test_depth: TestDepth, quote_enabled: TestQuoteEnabled) -> list[dict]:
    order_collection = list()

    if request_type == TestRequestType.VIDEO_AUTO:
        template = VIDEO_AUTO_TEMPLATE.copy()
    elif request_type == TestRequestType.ONLY_SCREENSHOTS:
        template = ONLY_SCREENSHOTS_TEMPLATE.copy()

    work_scoll_links = False
    quote_enabled = True if quote_enabled == TestQuoteEnabled.ENABLED else False

    if test_domains == TestDomains.ALL:
        social_domains = ('facebook', 'twitter', 'instagram', 'telegram')
        work_scoll_links = True
    elif test_domains == TestDomains.FACEBOOK:
        social_domains = ('facebook',)
    elif test_domains == TestDomains.TWITTER:
        social_domains = ('twitter',)
    elif test_domains == TestDomains.INSTAGRAM:
        social_domains = ('instagram',)
    elif test_domains == TestDomains.TELEGRAM:
        social_domains = ('telegram',)
    elif test_domains == TestDomains.SCROLL:
        work_scoll_links = True
    
    
    # parse social links
    for domain in social_domains:
        domain_links = SOCIAL_LINKS[domain]
        for link_collection in domain_links.values():
            depth_limit = 1 if test_depth == TestDepth.SMALL else len(domain_links.values())

            for idx in range(depth_limit):
                order = template.copy()
                order['link'] = link_collection[idx]
                order['link_type'] = domain
                order['quote_enabled'] = quote_enabled
                order["render_filename"] = f"tester-gfx-{secrets.token_hex(10)}.mp4"

                order_collection.append(order)

    # parse scroll links
    depth_limit = 1 if test_depth == TestDepth.SMALL else len(SCROLL_LINKS)
    for idx in range(depth_limit):
        order = template.copy()
        order['link'] = SCROLL_LINKS[idx]
        order['link_type'] = 'scroll'
        order['quote_enabled'] = quote_enabled
        order["render_filename"] = f"tester-gfx-{secrets.token_hex(10)}.mp4"

        order_collection.append(order)

    for order in order_collection:
        db_handler.add_db_entry(order)


def run_tests():
    create_server()
    create_test_orders(
        request_type=TestRequestType.VIDEO_AUTO,
        test_domains=TestDomains.FACEBOOK,
        test_depth=TestDepth.SMALL,
        quote_enabled=TestQuoteEnabled.ENABLED
    )

    process_screenshot_orders()
    render_video_orders()
    return True



