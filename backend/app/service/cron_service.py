import logging

from app.config.settings import settings
from app.data.repo.session_repo import SessionRepo

logger = logging.getLogger(__name__)


class CronService:
    def __init__(self, session_repo: SessionRepo):
        self.session_repo = session_repo

    async def delete_old_sessions(self) -> None:
        days = settings.cron_session_retention_days

        logger.info("Deleting expired sessions older than %d days...", days)

        count = await self.session_repo.delete_expired_older_than(days)

        logger.info("Deleted %d expired sessions older than %d days.", count, days)
