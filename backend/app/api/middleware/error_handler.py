import logging
import uuid

from app.exception.base_exception import BaseAppException
from app.model.error_model import ErrorResponse
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.exception_handler(BaseAppException)
    async def base_app_exception_handler(request: Request, exc: BaseAppException):
        logger.warning(
            f"[{exc.code}] {exc.message} | error_id={exc.error_id} | method={request.method} | path={request.url.path} | details={exc.details}"
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                code=exc.code,
                message=exc.message,
                error_id=exc.error_id,
                details=exc.details,
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        # Extract a clean field -> message map
        field_errors = {
            ".".join(str(part) for part in err["loc"][1:]): err["msg"]
            for err in exc.errors()
        }

        error_id = str(uuid.uuid4())
        logger.warning(
            f"[VALIDATION_ERROR] Invalid request | error_id={error_id} | path={request.url.path} | method={request.method} | details={field_errors}"
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(
                code="VALIDATION_ERROR",
                message="Invalid request data",
                error_id=error_id,
                details=field_errors,
            ).model_dump(),
        )
