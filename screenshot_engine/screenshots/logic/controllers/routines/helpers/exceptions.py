class MissingPostWorkflow(Exception):
    def __init__(self, url: str):
        self.url = url

    def __str__(self):
        return f"No POST workflow is available for this url: {self.url}"
