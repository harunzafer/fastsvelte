from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta


def get_current_quota_period(
    subscription_started_at: datetime, now: datetime = None
) -> tuple[datetime, datetime]:
    now = now or datetime.now(timezone.utc)

    # Determine how many full months have passed
    months_elapsed = 0
    temp_start = subscription_started_at
    while temp_start + relativedelta(months=1) <= now:
        temp_start += relativedelta(months=1)
        months_elapsed += 1

    period_start = subscription_started_at + relativedelta(months=months_elapsed)
    period_end = period_start + relativedelta(months=1)
    return period_start, period_end
