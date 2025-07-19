from app.exception.base_exception import BaseAppException


class UnknownSettingKey(BaseAppException):
    def __init__(self, setting_scope: str, key: str):
        super().__init__(
            code="UNKNOWN_SETTING_KEY",
            message=f"Unknown {setting_scope} setting key: {key}",
            status_code=400,
            details={"key": key, "scope": setting_scope},
        )


class InvalidSettingValue(BaseAppException):
    def __init__(self, expected_type: str, raw_value: str):
        super().__init__(
            code="INVALID_SETTING_VALUE",
            message=f"Invalid value for type {expected_type}",
            status_code=422,
            details={"expected_type": expected_type, "value": raw_value},
        )
