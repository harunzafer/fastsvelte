import uuid
from typing import Optional


class BaseAppException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int,
        details: Optional[dict] = None,
        error_id: Optional[str] = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        self.error_id = error_id or str(uuid.uuid4())

