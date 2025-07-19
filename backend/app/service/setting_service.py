import json

from app.data.repo.organization_setting_repo import OrganizationSettingRepo
from app.data.repo.setting_repo import SettingRepo
from app.data.repo.user_setting_repo import UserSettingRepo
from app.exception.setting_exception import InvalidSettingValue, UnknownSettingKey
from app.model.setting_model import (
    OrganizationSetting,
    SettingType,
    UserSetting,
)


class SettingService:
    def __init__(
        self,
        user_setting_repo: UserSettingRepo,
        organization_setting_repo: OrganizationSettingRepo,
        setting_repo: SettingRepo,
    ):
        self.user_setting_repo = user_setting_repo
        self.organization_setting_repo = organization_setting_repo
        self.setting_repo = setting_repo

    def _validate_value(self, value: str, setting_type: SettingType) -> None:
        try:
            match setting_type:
                case SettingType.boolean:
                    if value.lower() not in ("true", "false"):
                        raise ValueError()
                case SettingType.int:
                    int(value)
                case SettingType.float:
                    float(value)
                case SettingType.json:
                    json.loads(value)
                case SettingType.string:
                    pass
        except Exception:
            raise InvalidSettingValue(setting_type.value, value)

    async def set_user_setting_by_key(
        self, user_id: int, key: str, value: str
    ) -> UserSetting:
        definition = await self.setting_repo.get_user_setting_definition(key)
        if not definition:
            raise UnknownSettingKey("user", key)
        self._validate_value(value, definition.type)
        return await self.user_setting_repo.set_user_setting(
            user_id, definition.id, value
        )

    async def set_organization_setting_by_key(
        self, org_id: int, key: str, value: str
    ) -> OrganizationSetting:
        definition = await self.setting_repo.get_org_setting_definition(key)
        if not definition:
            raise UnknownSettingKey("organization", key)
        self._validate_value(value, definition.type)
        return await self.organization_setting_repo.set_organization_setting(
            org_id, definition.id, value
        )

    async def list_user_settings(self, user_id: int) -> list[UserSetting]:
        return await self.user_setting_repo.list_user_settings(user_id)

    async def list_organization_settings(
        self, organization_id: int
    ) -> list[OrganizationSetting]:
        return await self.organization_setting_repo.list_organization_settings(
            organization_id
        )
