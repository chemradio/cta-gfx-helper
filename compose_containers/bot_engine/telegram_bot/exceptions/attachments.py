class AttachmentNotNeeded(Exception):
    def __init__(self, message="Attachment not needed at this stage"):
        super().__init__(message)

class AttachmentTypeMismatch(Exception):
    def __init__(self, message="Attachment type mismatch"):
        super().__init__(message)

class AttachmentSizeExceeded(Exception):
    def __init__(self, message="Attachment size exceeded"):
        super().__init__(message)

class AttachmentNotFound(Exception):
    def __init__(self, message="Attachment not found"):
        super().__init__(message)