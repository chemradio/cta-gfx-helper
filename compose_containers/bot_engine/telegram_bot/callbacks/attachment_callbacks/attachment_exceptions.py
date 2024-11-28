import config


class AudioDurationExceeded(Exception):
    def __init__(self, duration, max_duration=config.MAX_AUDIO_LENGTH):
        self.duration = duration
        self.max_duration = max_duration
        super().__init__()

    def __str__(self):
        return f"Max audio duration of {self.max_duration} sec. exceeded. Supplied duration: {self.duration}"


class WrongAudioFormat(Exception):
    def __init__(
        self, format: str, supported_formats: list = ["audio/mpeg3", "audio/mpeg"]
    ):
        self.format = format
        self.supported_formats = supported_formats
        super().__init__()

    def __str__(self):
        return f"Audio format {self.format} is not supported. Supported formats: {self.supported_formats}"


class WrongImageFormat(Exception):
    def __init__(self, format: str):
        self.format = format
        super().__init__()

    def __str__(self):
        return f"Image format {self.format} is not supported."


class FailedConvertImage(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__()

    def __str__(self):
        return f"Image conversion failed with this error: {self.message}."
