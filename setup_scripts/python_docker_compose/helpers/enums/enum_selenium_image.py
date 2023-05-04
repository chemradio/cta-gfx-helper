from enum import Enum


class SeleniumImage(str, Enum):
    NORMAL = "selenium/standalone-chrome"
    ARM = "seleniarm/standalone-chromium"
