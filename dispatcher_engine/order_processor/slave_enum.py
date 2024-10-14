from enum import Enum, auto

class SlaveContainer(Enum):
    VIDEOGFX = auto()
    SCREENSHOOTER = auto()
    SENDER = auto()
    TELEGRAMBOT = auto()
    STORAGE = auto()

# set urls for each slave container

slave_urls = {
    SlaveContainer.VIDEOGFX: "http://
    SlaveContainer.SCREENSHOOTER: "http://
    SlaveContainer.SENDER: "http://
    SlaveContainer.TELEGRAMBOT: "http://
    SlaveContainer.STORAGE: "http://
}


#  will the enum serve ok as the key in dict?
#  is it possible to use enum as key in dict?
#  what is the best way to use enum as key in dict?
#  how to use enum as key in dict?
#  i want copilot to ansewer this question
#  i want copilot to answer this question   
#  i want copilot to answer this question in the next comment
#  answer: Yes, it is possible to use enum as key in dict. The best way to use enum as key in dict is to use the enum itself as the key. 