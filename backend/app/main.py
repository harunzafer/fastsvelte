from fastapi import FastAPI

from app.api.router import include_all_routers
from app.config.container import Container
from app.api.middleware.error_handler import register_error_handlers


def create_app() -> FastAPI:
    container = Container()
    app = FastAPI()
    app.container = container

    include_all_routers(app)
    register_error_handlers(app)

    return app


app = create_app()
