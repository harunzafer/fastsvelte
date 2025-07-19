from typing import Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: str                     # machine-readable code
    message: str                  # user-facing or developer-facing text
    details: Optional[dict] = None  # optional structured data
