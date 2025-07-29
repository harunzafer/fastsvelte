from app.config.container import Container
from app.config.settings import settings
from app.service.cron_service import CronService
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, HTTPException, status

router = APIRouter()


@router.post("/delete-old-sessions", status_code=204, include_in_schema=False)
@inject
async def delete_old_sessions(
    x_cron_secret: str = Header(..., alias="X-Cron-Secret"),
    cron_service: CronService = Depends(Provide[Container.cron_service]),
):
    if x_cron_secret != settings.cron_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    await cron_service.delete_old_sessions()
