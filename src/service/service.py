from client.client import Client
from lib.decorators.rate_limited import rate_limited
from lib.types.methods.groups_get_by_id import GroupsGetById
from lib.types.methods.wall_get import WallGet


class Service:
    RATE_LIMIT = 5

    def __init__(self, client: Client):
        self.client = client

    @rate_limited(RATE_LIMIT)
    def _execute_request(self, method, params):
        print("Request |", "method:", method, "params:", params)

        endpoint = f"/method/{method}"
        response = self.client.make_request(endpoint, params)
        print("Response |", response.status_code)

        if not response.ok:
            print("Error |", response.text)
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
