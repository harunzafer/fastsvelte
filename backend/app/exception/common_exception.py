from app.exception.base_exception import BaseAppException


class ResourceNotFound(BaseAppException):
    def __init__(self, resource: str, resource_id: int | str, details: dict = None):
        super().__init__(
            code="RESOURCE_NOT_FOUND",
            message=f"{resource.capitalize()} not found",
            status_code=404,
            details=details or {"resource": resource, "resource_id": resource_id},
        )
