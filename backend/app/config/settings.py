from typing import Literal, Optional

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    App-wide configuration using pydantic_settings.

    Environment variables:
    - Loaded from `.env` and the system
    - Must start with `FS_` (as per `env_prefix`)
    - Required fields must be present or the app will fail at startup

    Example:
        FS_APP_NAME -> settings.app_name
        FS_DB_URL -> settings.db_url
    """

    app_name: str = "My Super SAAS App"
    app_description: str = (
        "helps professionals like you work more efficiently with modern tools."
    )
    mode: Literal["b2c", "b2b"] = "b2c"
    environment: Literal["dev", "beta", "prod"] = "dev"
    db_url: str
    base_web_url: str = "http://localhost:5173"
    base_api_url: str = "http://localhost:8000"
    session_cookie_name: str = "session_id"
    session_cookie_max_age: int = 60 * 60 * 24  # 1 day
    session_refresh_threshold: int = int(session_cookie_max_age * 0.5)
    openai_api_key: str = None  # Should be set in .env
    stripe_api_key: str
    stripe_webhook_secret: str
    invitation_expiry_days: int = 7
    google_client_id: str
    google_client_secret: str
    jwt_secret_key: str
    # Cron Job related variables
    cron_secret: str
    cron_session_retention_days: int = 7

    # Email service configuration
    email_provider: Literal["stub", "azure", "sendgrid"] = "sendgrid"

    # Azure Email Service settings
    azure_email_connection_string: Optional[str] = None
    azure_email_sender_address: Optional[str] = None

    # SendGrid Email Service settings
    sendgrid_api_key: Optional[str] = None
    sendgrid_sender_address: Optional[str] = None
    sendgrid_sender_name: Optional[str] = None

    model_config = ConfigDict(
        env_file=".env",
        env_prefix="fs_",
        extra="ignore",  # allows extra env vars without failure
    )

    @property
    def cors_origins(self) -> list[str]:
        return {
            "dev": ["http://localhost:5173", "http://localhost:4173"],
            "beta": ["https://app-beta.example.com"],
            "prod": ["https://app.example.com"],
        }.get(self.environment, [])


# Load settings at app startup
settings = Settings()
