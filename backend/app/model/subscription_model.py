from pydantic import BaseModel


class PortalSessionResponse(BaseModel):
    url: str