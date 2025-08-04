from fastapi import APIRouter

router = APIRouter()


@router.get("/ping", operation_id="getPing")
async def ping() -> str:
    return "pong"
