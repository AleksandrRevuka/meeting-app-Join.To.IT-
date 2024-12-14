class InvalidPasswordError(Exception):
    """Exception raised when the provided password is invalid."""

    def __init__(self, message: str = "The password provided is invalid.") -> None:
        super().__init__(message)


class UserNotFoundUnAuthorizedError(Exception):
    """Raised when a user is not found or is unauthorized to perform a specific action."""

    def __init__(self, message: str = "User not found or unauthorized.") -> None:
        super().__init__(message)
