class InvalidPasswordError(Exception):
    """Exception raised when the provided password is invalid."""

    def __init__(self, message: str = "The password provided is invalid.") -> None:
        super().__init__(message)


class EmailNotConfirmedError(Exception):
    """Exception raised when the user's email is not confirmed."""

    def __init__(
        self, message: str = "Email not confirmed. Please verify your email address."
    ) -> None:
        super().__init__(message)


class InvalidRefreshTokenError(Exception):
    """Exception raised when the refresh token is invalid or expired."""

    def __init__(self, message: str = "The provided refresh token is invalid or expired.") -> None:
        super().__init__(message)


class InvalidTokenError(Exception):
    """Exception raised when an invalid token is used."""

    def __init__(self, message: str = "The token provided is invalid.") -> None:
        super().__init__(message)


class PasswordsNotMatchingError(Exception):
    """Exception raised when the new password and its confirmation do not match."""

    def __init__(self, message: str = "The new password and confirmation do not match.") -> None:
        super().__init__(message)


class EmailAlreadyConfirmedError(Exception):
    """Exception raised when trying to confirm an already confirmed email."""

    def __init__(self, message: str = "The email is already confirmed.") -> None:
        super().__init__(message)


class InvalidResetPasswordTokenError(Exception):
    """Exception raised when the reset password token is invalid or expired."""

    def __init__(
        self, message: str = "The reset password token is invalid or has expired."
    ) -> None:
        super().__init__(message)


class ForbiddenError(Exception):
    """Exception raised when access is forbidden to the requested resource."""

    def __init__(self, message: str = "Access to this resource is forbidden.") -> None:
        super().__init__(message)


class UserNotFoundUnAuthorizedError(Exception):
    """Raised when a user is not found or is unauthorized to perform a specific action."""

    def __init__(self, message: str = "User not found or unauthorized.") -> None:
        super().__init__(message)
