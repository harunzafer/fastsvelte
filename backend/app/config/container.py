from app.config.settings import settings
from app.data.db_config import DatabaseConfig
from app.data.repo.email_verification_repo import EmailVerificationRepo
from app.data.repo.note_repo import NoteRepo
from app.data.repo.org_repo import OrgRepo
from app.data.repo.organization_setting_repo import OrganizationSettingRepo
from app.data.repo.password_repo import PasswordRepo
from app.data.repo.session_repo import SessionRepo
from app.data.repo.setting_repo import SettingRepo
from app.data.repo.user_repo import UserRepo
from app.data.repo.user_setting_repo import UserSettingRepo
from app.service.auth_service import AuthService
from app.service.email_service_stub import StubEmailService
from app.service.email_verification_service import EmailVerificationService
from app.service.note_service import NoteService
from app.service.openai_service import OpenAIService
from app.service.password_service import PasswordService
from app.service.setting_service import SettingService
from app.service.summary_service import SummaryService
from app.service.user_service import UserService
from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    db_config = providers.Singleton(DatabaseConfig, dsn=settings.db_url)

    user_repo = providers.Singleton(UserRepo, db_config=db_config)
    org_repo = providers.Singleton(OrgRepo, db_config=db_config)
    session_repo = providers.Singleton(SessionRepo, db_config=db_config)
    password_repo = providers.Singleton(PasswordRepo, db_config=db_config)
    note_repo = providers.Singleton(NoteRepo, db_config=db_config)
    setting_repo = providers.Factory(
        SettingRepo,
        db_config=db_config,
    )
    email_verification_repo = providers.Factory(
        EmailVerificationRepo,
        db_config=db_config,
    )

    user_setting_repo = providers.Factory(
        UserSettingRepo,
        db_config=db_config,
    )

    organization_setting_repo = providers.Factory(
        OrganizationSettingRepo,
        db_config=db_config,
    )

    setting_service = providers.Factory(
        SettingService,
        user_setting_repo=user_setting_repo,
        organization_setting_repo=organization_setting_repo,
        setting_repo=setting_repo,
    )

    email_service = providers.Singleton(StubEmailService)
    email_verification_service = providers.Factory(
        EmailVerificationService,
        email_service=email_service,
        email_verification_repo=email_verification_repo,
        user_repo=user_repo,
    )
    openai_service = providers.Factory(
        OpenAIService,
        model="gpt-4o-mini",
        temperature=0.1,
        api_key=settings.openai_api_key,
    )

    summary_service = providers.Factory(
        SummaryService,
        openai_service=openai_service,
    )

    user_service = providers.Factory(UserService, user_repo=user_repo)
    auth_service = providers.Factory(
        AuthService,
        user_repo=user_repo,
        session_repo=session_repo,
        org_repo=org_repo,
        email_verification_service=email_verification_service,
    )
    password_service = providers.Factory(
        PasswordService,
        user_repo=user_repo,
        password_repo=password_repo,
        email_service=email_service,
    )

    note_service = providers.Factory(
        NoteService,
        note_repo=note_repo,
        summary_service=summary_service,
    )

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.middleware.auth_handler",
            "app.api.route.user_route",
            "app.api.route.auth_route",
            "app.api.route.password_route",
            "app.api.route.note_route",
            "app.api.route.setting_route",
            "app.api.route.email_verification_route",
        ]
    )
