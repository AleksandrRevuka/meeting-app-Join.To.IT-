from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    message: str = Field(examples=["User not found"])
    exception: str | None = Field(
        examples=["UserNotFoundUnAuthorizedError: User not found or unauthorized."],
        default=None,
    )
    error: bool = Field(examples=["true"], default=True, frozen=True)

    @classmethod
    def respond(cls, message: str, exception: str | None = None) -> dict[str, str]:
        return cls(message=message, exception=exception).model_dump()
