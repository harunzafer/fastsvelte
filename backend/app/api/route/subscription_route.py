from app.api.middleware.auth_handler import min_role_required
from app.config.container import Container
from app.config.settings import settings
from app.data.repo.plan_repo import PlanRepo
from app.model.role_model import Role
from app.model.user_model import CurrentUser
from app.service.stripe_service import StripeService
from app.service.subscription_service import SubscriptionService
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post("/manage", operation_id="manageSubscription")
@inject
async def create_portal_session(
    user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
    subscription_service: SubscriptionService = Depends(
        Provide[Container.subscription_service]
    ),
) -> dict:
    url = await subscription_service.get_portal_url_for_org(user.organization_id)
    return {"url": url}


# @router.post("/start_checkout", operation_id="startCheckout")
# @inject
# async def start_checkout(
#     plan_id: int,
#     user: CurrentUser = Depends(min_role_required(Role.MEMBER)),
#     plan_repo: PlanRepo = Depends(Provide[Container.plan_repo]),
#     stripe_service: StripeService = Depends(Provide[Container.stripe_service]),
# ) -> dict:
#     plan = await plan_repo.get_by_id(plan_id)
#     if not plan or not plan.stripe_product_id:
#         raise HTTPException(
#             status_code=400, detail="Invalid plan or missing Stripe product"
#         )

#     customer_id = (
#         user.session.stripe_customer_id
#         or await stripe_service.get_customer_id_for_org(user.organization_id)
#     )
#     if not customer_id:
#         raise HTTPException(status_code=400, detail="Stripe customer not found")

#     try:
#         url = stripe_service.create_checkout_session(
#             customer_id, plan.stripe_product_id, settings.base_web_url
#         )
#         return {"url": url}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
