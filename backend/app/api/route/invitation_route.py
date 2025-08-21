from app.api.middleware.auth_handler import min_role_required
from app.config.container import Container
from app.exception.invitation_exception import InvalidOrExpiredInvitation
from app.model.invitation_model import (
    InvitationAcceptRequest,
    InvitationCreateRequest,
    InvitationResponse,
)
from app.model.role_model import Role
from app.model.user_model import CurrentUser
from app.service.email_service_base import EmailService
from app.service.invitation_service import InvitationService
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, BackgroundTasks, Depends

router = APIRouter()


@router.post("/", response_model=InvitationResponse, operation_id="createInvitation")
@inject
async def create_invitation(
    request: InvitationCreateRequest,
    background_tasks: BackgroundTasks,
    user: CurrentUser = Depends(min_role_required(Role.ORG_ADMIN)),
    invitation_service: InvitationService = Depends(
        Provide[Container.invitation_service]
    ),
    email_service: EmailService = Depends(Provide[Container.email_service]),
):
    email = request.email.strip().lower()

    if user.role == Role.SYSTEM_ADMIN:
        org_id = None
    else:
        org_id = user.organization_id

    invitation, invite_link = await invitation_service.create_invitation(
        email=email,
        role=request.role,
        organization_id=org_id,
        created_by=user.id,
    )

    background_tasks.add_task(
        email_service.send_invitation_email,
        invitation.email,
        invite_link,
    )

    return InvitationResponse.model_validate(invitation.model_dump())


@router.get(
    "/pending",
    response_model=list[InvitationResponse],
    operation_id="getPendingInvitations",
)
@inject
async def get_pending_invitations(
    user: CurrentUser = Depends(min_role_required(Role.ORG_ADMIN)),
    invitation_service: InvitationService = Depends(
        Provide[Container.invitation_service]
    ),
):
    if user.role == Role.SYSTEM_ADMIN:
        invitations = await invitation_service.get_all_pending_invitations()
    else:
        invitations = await invitation_service.get_pending_invitations(
            user.organization_id
        )
    return [InvitationResponse.model_validate(inv.model_dump()) for inv in invitations]


@router.get(
    "/{invitation_id}",
    response_model=InvitationResponse,
    operation_id="getInvitationStatus",
)
@inject
async def get_invitation_status(
    invitation_id: int,
    user: CurrentUser = Depends(min_role_required(Role.ORG_ADMIN)),
    invitation_service: InvitationService = Depends(
        Provide[Container.invitation_service]
    ),
):
    invitation = await invitation_service.get_invitation(
        invitation_id, user.organization_id
    )
    return InvitationResponse.model_validate(invitation.model_dump())


@router.delete("/{invitation_id}", operation_id="revokeInvitation")
@inject
async def revoke_invitation(
    invitation_id: int,
    user: CurrentUser = Depends(min_role_required(Role.ORG_ADMIN)),
    invitation_service: InvitationService = Depends(
        Provide[Container.invitation_service]
    ),
):
    print(
        f"Revoking invitation {invitation_id} for user {user.id}, organization {user.organization_id}"
    )
    await invitation_service.revoke_invitation(invitation_id, user.organization_id)
    return {"message": "Invitation revoked"}


@router.post("/accept", operation_id="acceptInvitation")
@inject
async def accept_invitation(
    request: InvitationAcceptRequest,
    invitation_service: InvitationService = Depends(
        Provide[Container.invitation_service]
    ),
):
    success = await invitation_service.accept_invitation(
        token=request.token,
        password=request.password,
        first_name=request.first_name,
        last_name=request.last_name,
        organization_name=request.organization_name,
    )
    if not success:
        raise InvalidOrExpiredInvitation()
    return {"message": "Invitation accepted"}
