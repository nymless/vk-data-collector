from typing import TypedDict

from src.lib.types.objects.group import Group
from src.lib.types.objects.user import User


class Response(TypedDict):
    groups: list[Group]
    # extended flag
    profiles: list[User]


class GroupsGetById(TypedDict):
    """https://dev.vk.com/ru/method/groups.getById"""

    response: Response
