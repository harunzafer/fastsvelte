from app.exception.base_exception import BaseAppException


class Unauthorized(BaseAppException):
    def __init__(self, message="Missing or invalid session token", details=None):
        super().__init__(
            code="UNAUTHORIZED",
            message=message,
            status_code=401,
            details=details,
        )


class AccessDenied(BaseAppException):
    def __init__(self, message="Access denied", details=None):
        super().__init__(
            code="ACCESS_DENIED",
            message=message,
            status_code=403,
            details=details,
        )


class EmailAlreadyExists(BaseAppException):
    def __init__(self, details: dict = None):
        super().__init__(
            code="EMAIL_ALREADY_EXISTS",
            message="Email is already in use",
            status_code=409,
            details=details,
        )


class SignupFailed(BaseAppException):
    def __init__(self, details: dict = None):
        super().__init__(
            code="SIGNUP_FAILED",
            message="Signup failed",
            status_code=500,
            details=details,
        )


class EmailAlreadyVerified(BaseAppException):
    def __init__(self, details: dict = None):
        super().__init__(
            code="EMAIL_ALREADY_VERIFIED",
            message="Email already verified",
            status_code=400,
            details=details,
        )


class EmailNotVerified(BaseAppException):
    def __init__(self, details: dict = None):
        super().__init__(
            code="EMAIL_NOT_VERIFIED",
            message="Email not verified",
            status_code=403,
            details=details,
        )


class InvalidVerificationToken(BaseAppException):
    def __init__(self, details: dict = None):
        super().__init__(
            code="INVALID_VERIFICATION_TOKEN",
            message="Invalid or expired verification token",
            status_code=403,
            details=details,
        )


class InvalidCredentials(BaseAppException):
    def __init__(self, details: dict = None):
        super().__init__(
            code="INVALID_CREDENTIALS",
            message="Invalid email or password",
            status_code=401,
            details=details,
        )
