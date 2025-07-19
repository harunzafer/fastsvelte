from app.exception.base_exception import BaseAppException


class PasswordResetTokenInvalid(BaseAppException):
    def __init__(self, details: dict = None):
        super().__init__(
            code="INVALID_PASSWORD_RESET_TOKEN",
            message="Invalid or expired password reset token",
            status_code=403,
            details=details,
        )


class PasswordResetNotAllowed(BaseAppException):
    def __init__(self, details: dict = None):
        super().__init__(
            code="PASSWORD_RESET_NOT_ALLOWED",
            message="Password reset is not allowed for this user",
            status_code=400,
            details=details,
        )
