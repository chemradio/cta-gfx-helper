from dataclasses import dataclass


class PostXpaths:
    def __init__(self, logged_in: bool=False) -> None:
        self.logged_in = logged_in

    
    @property
    def facebook_post_xpath(self) -> str:
        if self.logged_in:
            return "//div[@class='g4tp4svg om3e55n1']"
        else:
            return "//div[@role='article']"

    