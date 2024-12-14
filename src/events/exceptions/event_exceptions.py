class ForbiddenError(Exception):
    """Exception raised when access is forbidden to the requested resource."""

    def __init__(self, message: str = "Access to this resource is forbidden.") -> None:
        super().__init__(message)

class EventNotFoundError(Exception):
    """Exception raised when the event is not found in the system."""

    def __init__(self, message: str = "Event not found.") -> None:
        super().__init__(message)


class RegistrationAlreadyExistsError(Exception):
    """Exception raised when a user tries to register for an event
    they are already registered for."""

    def __init__(self, message: str = "Registration already exists for this event.") -> None:
        super().__init__(message)