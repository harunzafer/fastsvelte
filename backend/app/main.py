import logging

from app.api.middleware.error_handler import register_error_handlers
from app.api.router import include_all_routers
from app.config.container import Container
from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)


def create_app() -> FastAPI:
    container = Container()
    app = FastAPI()
    app.container = container

    include_all_routers(app)
    register_error_handlers(app)

    return app


app = create_app()
