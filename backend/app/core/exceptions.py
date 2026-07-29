class StudioPilotException(Exception):
    """Base application exception."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundException(StudioPilotException):
    pass


class BadRequestException(StudioPilotException):
    pass


class ConflictException(StudioPilotException):
    pass