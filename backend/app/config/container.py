from app.config.settings import settings
from app.data.db_config import DatabaseConfig
from app.data.repo.org_repo import OrgRepo
from app.data.repo.session_repo import SessionRepo
from app.data.repo.user_repo import UserRepo
from app.service.auth_service import AuthService
from app.service.user_service import UserService
from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    db_config = providers.Singleton(DatabaseConfig, dsn=settings.db_url)

    user_repo = providers.Singleton(UserRepo, db_config=db_config)
    org_repo = providers.Singleton(OrgRepo, db_config=db_config)
    session_repo = providers.Singleton(SessionRepo, db_config=db_config)

    user_service = providers.Singleton(UserService, user_repo=user_repo)
    auth_service = providers.Factory(
        AuthService,
        user_repo=user_repo,
        session_repo=session_repo,
        org_repo=org_repo,
    )

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.middleware.auth_handler",
            "app.api.route.user_route",
            "app.api.route.auth_route",
        ]
    )
