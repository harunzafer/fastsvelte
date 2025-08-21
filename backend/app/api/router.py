from app.api.route.auth_route import router as auth_router
from app.api.route.cron_route import router as cron_router
from app.api.route.email_verification_route import router as email_verification_router
from app.api.route.invitation_route import router as invitation_router
from app.api.route.note_route import router as note_router
from app.api.route.password_route import router as password_router
from app.api.route.ping_route import router as ping_router
from app.api.route.plan_route import router as plan_router
from app.api.route.setting_route import router as setting_router
from app.api.route.stats_route import router as stats_router
from app.api.route.stripe_webhook_route import router as stripe_webhook_route
from app.api.route.subscription_route import router as subscription_route
from app.api.route.user_route import router as user_router
from app.config.settings import settings
from fastapi import FastAPI


def include_all_routers(app: FastAPI):
    app.include_router(user_router, prefix="/users", tags=["Users"])
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    app.include_router(
        email_verification_router,
        prefix="/auth",
        tags=["Email Verification"],
    )
    app.include_router(
        password_router, prefix="/password", tags=["Password Management"]
    )
    app.include_router(note_router, prefix="/notes", tags=["Notes"])
    app.include_router(setting_router, prefix="/settings", tags=["Settings"])
    app.include_router(stats_router, prefix="/stats", tags=["Statistics"])
    app.include_router(plan_router, prefix="/plan", tags=["Plan"])
    app.include_router(
        stripe_webhook_route, prefix="/webhooks", tags=["Stripe Webhook"]
    )
    app.include_router(cron_router, prefix="/cron", tags=["Cron Job"])
    app.include_router(
        subscription_route, prefix="/subscription", tags=["Subscription"]
    )
    if settings.mode == "b2b":
        app.include_router(
            invitation_router, prefix="/invitations", tags=["Invitations"]
        )

    app.include_router(ping_router, prefix="", tags=["Ping"])
