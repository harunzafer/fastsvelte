from typing import ClassVar

from pydantic import BaseModel


class Role(BaseModel):
    name: str
    precedence: int

    class Config:
        frozen = True  # makes it immutable and hashable

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Role):
            return NotImplemented
        return self.name == other.name

    def __lt__(self, other: "Role") -> bool:
        return self.precedence < other.precedence

    def __le__(self, other: "Role") -> bool:
        return self.precedence <= other.precedence

    def __gt__(self, other: "Role") -> bool:
        return self.precedence > other.precedence

    def __ge__(self, other: "Role") -> bool:
        return self.precedence >= other.precedence

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Role({self.name!r}, {self.precedence})"

    # Predefined roles. Update here before adding new roles to the database
    READONLY: ClassVar["Role"] = None  # placeholder for below
    MEMBER: ClassVar["Role"] = None
    ORG_ADMIN: ClassVar["Role"] = None
    SYSTEM_ADMIN: ClassVar["Role"] = None

    # Role registry
    _all_roles: ClassVar[dict[str, "Role"]] = {}

    @classmethod
    def get(cls, name: str) -> "Role":
        return cls._all_roles[name]

    @classmethod
    def all(cls) -> list["Role"]:
        return list(cls._all_roles.values())


# Set predefined roles after class definition. Update before adding new roles to the database
Role.READONLY = Role(name="readonly", precedence=0)
Role.MEMBER = Role(name="member", precedence=1)
Role.ORG_ADMIN = Role(name="org_admin", precedence=2)
Role.SYSTEM_ADMIN = Role(name="system_admin", precedence=3)

Role._all_roles = {
    "readonly": Role.READONLY,
    "member": Role.MEMBER,
    "org_admin": Role.ORG_ADMIN,
    "system_admin": Role.SYSTEM_ADMIN,
}
