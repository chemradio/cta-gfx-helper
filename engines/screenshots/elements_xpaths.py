from dataclasses import dataclass


class PostXpaths:
    def __init__(self) -> None:
        pass

    def facebook_post_xpath(self, logged_in: bool=True) -> str:
        if logged_in:
            return "//div[@class='g4tp4svg om3e55n1']"
        else:
            return