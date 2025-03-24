from typing import TypedDict

from lib.types.objects.comment import Comment


class Thread(TypedDict):
    count: int
    items: list[Comment]
    can_post: bool
    show_reply_button: bool
    groups_can_post: bool
    next_from: str
