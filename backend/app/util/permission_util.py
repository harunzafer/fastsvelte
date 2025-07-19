from app.exception.auth_exception import AccessDenied
from app.model.role_model import Role
from app.model.user_model import CurrentUser, User


def require_same_org_or_admin(actor: CurrentUser, target: User, action: str = "perform this action") -> None:
    """
    Raises AccessDenied if actor is not SYSTEM_ADMIN and is not in the same org as the target.
    """
    if actor.role == Role.SYSTEM_ADMIN:
        return

    if actor.role != Role.ORG_ADMIN or actor.organization_id != target.organization_id:
        raise AccessDenied(f"Not authorized to {action} for this user")
