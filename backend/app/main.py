import logging

from app.api.middleware.error_handler import register_error_handlers
from app.api.router import include_all_routers
from app.config.container import Container
from app.config.settings import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)


def configure_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    container = Container()
    app = FastAPI()
    app.container = container

    configure_cors(app)
    include_all_routers(app)
    register_error_handlers(app)

    return app


app = create_app()
