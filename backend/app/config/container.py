from app.config.settings import settings
from app.data.db_config import DatabaseConfig
from app.data.repo.email_verification_repo import EmailVerificationRepo
from app.data.repo.invitation_repo import InvitationRepo
from app.data.repo.note_repo import NoteRepo
from app.data.repo.organization_plan_repo import OrganizationPlanRepo
from app.data.repo.organization_repo import OrganizationRepo
from app.data.repo.organization_setting_repo import OrganizationSettingRepo
from app.data.repo.organization_usage_repo import OrganizationUsageRepo
from app.data.repo.password_repo import PasswordRepo
from app.data.repo.plan_repo import PlanRepo
from app.data.repo.session_repo import SessionRepo
from app.data.repo.setting_repo import SettingRepo
from app.data.repo.user_repo import UserRepo
from app.data.repo.user_setting_repo import UserSettingRepo
from app.service.auth_service import AuthService
from app.service.cron_service import CronService
from app.service.email_service_factory import create_email_service
from app.service.email_verification_service import EmailVerificationService
from app.service.invitation_service import InvitationService
from app.service.note_service import NoteService
from app.service.onboarding_service import OnboardingService
from app.service.openai_service import OpenAIService
from app.service.organization_usage_service import OrganizationUsageService
from app.service.password_service import PasswordService
from app.service.plan_service import PlanService
from app.service.setting_service import SettingService
from app.service.stripe_service import StripeService
from app.service.subscription_service import SubscriptionService
from app.service.note_organizer_service import NoteOrganizerService
from app.service.user_service import UserService
from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    db_config = providers.Singleton(DatabaseConfig, dsn=settings.db_url)

    # Repositories
    user_repo = providers.Singleton(UserRepo, db_config=db_config)
    organization_repo = providers.Singleton(OrganizationRepo, db_config=db_config)
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
    plan_repo = providers.Factory(PlanRepo, db_config=db_config)

    organization_plan_repo = providers.Factory(
        OrganizationPlanRepo,
        db_config=db_config,
    )
    organization_usage_repo = providers.Factory(
        OrganizationUsageRepo, db_config=db_config
    )

    # Repos
    invitation_repo = providers.Factory(
        InvitationRepo,
        db_config=db_config,
    )

    organization_usage_service = providers.Factory(
        OrganizationUsageService,
        usage_repo=organization_usage_repo,
        plan_repo=plan_repo,
        organization_plan_repo=organization_plan_repo,
    )
    subscription_service = providers.Factory(
        SubscriptionService,
        organization_repo=organization_repo,
        plan_repo=plan_repo,
        organization_plan_repo=organization_plan_repo,
    )

    # Stripe Service
    stripe_service = providers.Factory(
        StripeService,
        api_key=settings.stripe_api_key,
        webhook_secret=settings.stripe_webhook_secret,
    )

    # Subscription Service
    subscription_service = providers.Factory(
        SubscriptionService,
        organization_repo=organization_repo,
        plan_repo=plan_repo,
        organization_plan_repo=organization_plan_repo,
        stripe_service=stripe_service,
    )

    # Onboarding Service
    onboarding_service = providers.Factory(
        OnboardingService,
        organization_repo=organization_repo,
        organization_plan_repo=organization_plan_repo,
        subscription_service=subscription_service,
    )

    # Services
    setting_service = providers.Factory(
        SettingService,
        user_setting_repo=user_setting_repo,
        organization_setting_repo=organization_setting_repo,
        setting_repo=setting_repo,
    )

    email_service = providers.Singleton(create_email_service)
    email_verification_service = providers.Factory(
        EmailVerificationService,
        email_service=email_service,
        email_verification_repo=email_verification_repo,
        user_repo=user_repo,
    )

    invitation_service = providers.Factory(
        InvitationService,
        invitation_repo=invitation_repo,
        user_repo=user_repo,
        org_repo=organization_repo,
    )

    openai_service = providers.Factory(
        OpenAIService,
        model="gpt-4o-mini",
        temperature=0.1,
        api_key=settings.openai_api_key,
    )

    note_organizer_service = providers.Factory(
        NoteOrganizerService,
        openai_service=openai_service,
    )

    user_service = providers.Factory(UserService, user_repo=user_repo)
    auth_service = providers.Factory(
        AuthService,
        user_repo=user_repo,
        session_repo=session_repo,
        org_repo=organization_repo,
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
        note_organizer_service=note_organizer_service,
    )

    cron_service = providers.Factory(
        CronService,
        session_repo=session_repo,
    )

    plan_service = providers.Factory(PlanService, plan_repo=plan_repo)

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.middleware.auth_handler",
            "app.api.route.user_route",
            "app.api.route.auth_route",
            "app.api.route.password_route",
            "app.api.route.note_route",
            "app.api.route.setting_route",
            "app.api.route.email_verification_route",
            "app.api.route.plan_route",
            "app.api.route.subscription_route",
            "app.api.route.stripe_webhook_route",
            "app.api.route.invitation_route",
            "app.api.route.cron_route",
            "app.api.route.stats_route",
        ]
    )
