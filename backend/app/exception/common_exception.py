from app.exception.base_exception import BaseAppException


class ResourceNotFound(BaseAppException):
    def __init__(
        self,
        resource: str,
        resource_id: int | str,
        details: dict = None,
        message: str = None,
    ):
        super().__init__(
            code="RESOURCE_NOT_FOUND",
            message=message if message else f"{resource.capitalize()} not found",
            status_code=404,
            details=details or {"resource": resource, "resource_id": resource_id},
        )


class QuotaExceeded(BaseAppException):
    def __init__(
        self, feature_key: str, limit: int | None = None, details: dict = None
    ):
        message = f"Quota exceeded for feature '{feature_key}'"
        if limit is not None:
            message += f" (limit: {limit})"

        super().__init__(
            code="QUOTA_EXCEEDED",
            message=message,
            status_code=403,
            details=details or {"feature_key": feature_key, "limit": limit},
        )
