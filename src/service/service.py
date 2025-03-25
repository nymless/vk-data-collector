from client.client import Client
from lib.decorators.rate_limited import rate_limited
from lib.types.methods.groups_get_by_id import GroupsGetById
from lib.types.methods.wall_get import WallGet
from lib.types.methods.wall_get_comments import WallGetComments


class Service:
    RATE_LIMIT = 4

    def __init__(self, client: Client):
        self.client = client

    @rate_limited(RATE_LIMIT)
    def _execute_request(self, method, params):
        print("REQUEST:", "method:", method, "params:", params)
        endpoint = f"/method/{method}"
        response = self.client.make_request(endpoint, params)
        print("RESPONSE:", response.status_code)
        if not response.ok:
            print("ERROR:", response.text)
            raise Exception("Response Error")
        return response.json()

    def get_wall_posts_by_domain(self, domain: str, **params) -> WallGet:
        method = "wall.get"
        params["domain"] = domain
        return self._execute_request(method, params)

    def get_groups_by_ids(self, ids: str, **params) -> GroupsGetById:
        method = "groups.getById"
        params["group_ids"] = ids
        return self._execute_request(method, params)

    def get_groups_by_domains(self, domains: str, **params) -> GroupsGetById:
        return self.get_groups_by_ids(domains, **params)

    def get_comments_by_wall_post(
        self, owner_id: int, post_id: int, **params
    ) -> WallGetComments:
        method = "wall.getComments"
        params["owner_id"] = owner_id
        params["post_id"] = post_id
        return self._execute_request(method, params)

    def get_thread_by_comment(
        self, owner_id: int, post_id: int, comment_id: int, **params
    ) -> WallGetComments:
        method = "wall.getComments"
        params["owner_id"] = owner_id
        params["post_id"] = post_id
        params["comment_id"] = comment_id
        return self._execute_request(method, params)
