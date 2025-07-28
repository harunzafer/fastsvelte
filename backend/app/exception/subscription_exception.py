from app.exception.base_exception import BaseAppException


class OrganizationNotFound(BaseAppException):
    def __init__(self, stripe_customer_id: str):
        super().__init__(
            code="ORG_NOT_FOUND",
            message="Organization not found",
            status_code=404,
            details={"stripe_customer_id": stripe_customer_id},
        )


class PlanNotFound(BaseAppException):
    def __init__(self, stripe_product_id: str):
        super().__init__(
            code="PLAN_NOT_FOUND",
            message="Plan not found",
            status_code=404,
            details={"stripe_product_id": stripe_product_id},
        )


class NoDefaultPlan(BaseAppException):
    def __init__(self):
        super().__init__(
            code="NO_DEFAULT_PLAN",
            message="No default plan is configured",
            status_code=500,
        )


class DefaultPlanNotFree(BaseAppException):
    def __init__(self, plan_id: int):
        super().__init__(
            code="DEFAULT_PLAN_NOT_FREE",
            message="Default plan is not free and cannot be auto-subscribed",
            status_code=400,
            details={"plan_id": plan_id},
        )


class StripeCustomerNotFound(BaseAppException):
    def __init__(self, org_id: int):
        super().__init__(
            code="STRIPE_CUSTOMER_NOT_FOUND",
            message="Stripe customer ID is missing for this organization",
            status_code=400,
            details={"organization_id": org_id},
        )
