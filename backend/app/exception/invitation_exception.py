from app.exception.base_exception import BaseAppException


class InvalidOrExpiredInvitation(BaseAppException):
    def __init__(self):
        super().__init__(
            code="INVALID_INVITATION",
            message="Invalid or expired invitation",
            status_code=400,
        )
