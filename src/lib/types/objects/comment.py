from typing import Any, TypedDict

from lib.types.objects.donut import Donut
from lib.types.objects.thread import Thread


class Comment(TypedDict):
    id: int
    from_id: int
    date: int
    text: str
    donut: Donut
    reply_to_user: int
    reply_to_comment: int
    attachments: list[dict[str, Any]]
    parents_stack: list[Any]
    thread: Thread
