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


class InvalidFileTypeError(Exception):
    """Exception raised when the uploaded file type is invalid."""

    def __init__(
        self, message: str = "The file type is invalid. Please upload a valid file format."
    ) -> None:
        super().__init__(message)


class FileTooLargeError(Exception):
    """Exception raised when the uploaded file exceeds the maximum allowed size."""

    def __init__(self, message: str = "The file size exceeds the maximum allowed limit.") -> None:
        super().__init__(message)


class CloudinaryUploadFailedError(Exception):
    """Exception raised when a general Cloudinary upload fails."""

    def __init__(self, message: str = "Cloudinary upload failed.") -> None:
        super().__init__(message)


class CloudinaryFailedUploadAvatarError(Exception):
    """Exception raised when uploading an avatar to Cloudinary fails."""

    def __init__(self, message: str = "Failed to upload avatar to Cloudinary.") -> None:
        super().__init__(message)


class OldPasswordNotCorrectError(Exception):
    """Exception raised when the old password does not match."""

    def __init__(self, message: str = "The old password is incorrect.") -> None:
        super().__init__(message)


class NewPasswordNotMatchError(Exception):
    """Exception raised when the new password confirmation does not match."""

    def __init__(self, message: str = "New password and confirmation do not match.") -> None:
        super().__init__(message)


class WarningProfileUpdateError(Exception):
    """Exception raised when there is a warning during profile update."""

    def __init__(self, message: str = "Profile update encountered a warning.") -> None:
        super().__init__(message)


class UserAlreadyBannedError(Exception):
    """Exception raised when trying to ban a user who is already banned."""

    def __init__(self, message: str = "User has already been banned.") -> None:
        super().__init__(message)


class UserBannedError(Exception):
    """Exception raised when the user is banned."""

    def __init__(self, message: str = "This user is banned.") -> None:
        super().__init__(message)


class UserNotBannedError(Exception):
    """Exception raised when trying to activate a user who is not banned."""

    def __init__(self, message: str = "User is not banned.") -> None:
        super().__init__(message)


class CannotBanYourselfError(Exception):
    """Exception raised when a user attempts to ban themselves."""

    def __init__(self, message: str = "You cannot ban yourself.") -> None:
        super().__init__(message)


class NewRoleNotSpecifiedError(Exception):
    """Exception raised when no new role is specified for a role change action."""

    def __init__(self, message: str = "New role must be specified for changing role.") -> None:
        super().__init__(message)


class ForbiddenRoleChangeError(Exception):
    """Exception raised when trying to assign a forbidden role."""

    def __init__(self, message: str = "You don't have permission to change user roles.") -> None:
        super().__init__(message)


class PermissionDeniedError(Exception):
    """Exception raised when a user does not have permission for a certain action."""

    def __init__(self, message: str = "You don't have permission for this action.") -> None:
        super().__init__(message)
