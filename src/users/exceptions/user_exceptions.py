class UserWithEmailAlreadyExistsError(Exception):
    """Exception raised when a user with the same email already exists."""

    def __init__(self, message: str = "A user with this email already exists.") -> None:
        super().__init__(message)


class UserWithPhoneAlreadyExistsError(Exception):
    """Exception raised when a user with the same phone number already exists."""

    def __init__(self, message: str = "A user with this phone number already exists.") -> None:
        super().__init__(message)


class UserNotFoundError(Exception):
    """Exception raised when the user is not found in the system."""

    def __init__(self, message: str = "User not found.") -> None:
        super().__init__(message)
