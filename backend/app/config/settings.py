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

    app_name: str = "BrokerGuard"
    environment: str = "dev"
    db_url: str
    session_cookie_name: str = "session_id"
    session_cookie_max_age: int = 60 * 60 * 24  # 1 day
    session_refresh_threshold: int = int(session_cookie_max_age * 0.5)

    model_config = ConfigDict(
        env_file=".env",
        env_prefix="fs_",
        extra="ignore",  # allows extra env vars without failure
    )


# Load settings at app startup
settings = Settings()
