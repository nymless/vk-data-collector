import json
import os
import sys
from pathlib import Path
from typing import overload

from service.service import Service


class Collector:
    def __init__(self, service: Service):
        self.service = service
        self.encoding = sys.getdefaultencoding()

    @overload
    def collect_all_posts(self, domain: str, path: str) -> None:
        response = self.service.get_wall_posts_by_domain(domain, count=1)
        posts_path = Path(path)
        posts_path.mkdir(parents=True, exist_ok=True)

        count = response["response"]["count"]
        offset = 100
        runs = (count + offset - 1) // offset

        for i in range(runs):
            response = self.service.get_wall_posts_by_domain(
                domain, count=100, offset=offset * i
            )
            items = response["response"]["items"]

            # Make chunk json files
            chunk_path = posts_path.joinpath(f"{domain}_posts_{i}.json")
            with open(chunk_path, "w", encoding=self.encoding) as f:
                json.dump(items, f, ensure_ascii=False)

        # Make joint json file
        file_path = posts_path.joinpath(f"{domain}_posts.json")
        with open(file_path, "w", encoding=self.encoding) as f:
            posts = []
            for i in range(runs):
                chunk_path = posts_path.joinpath(f"{domain}_posts_{i}.json")
                with open(chunk_path, "r", encoding=self.encoding) as fp:
                    items = json.load(fp)
                    posts.extend(items)
            json.dump(posts, f, ensure_ascii=False)

        # Remove chunk json files
        for i in range(runs):
            chunk_path = posts_path.joinpath(f"{domain}_posts_{i}.json")
            os.remove(chunk_path)

    @overload
    def collect_all_posts(self, domains: list[str], path: str) -> None:
        for domain in domains:
            self.collect_all_posts(domain, path)

    def collect_groups(self, domains: list[str], path: str) -> None:
        groups_path = Path(path)
        groups_path.mkdir(parents=True, exist_ok=True)

        fields = (
            "activity,wall,city,description,cover,members_count,place,site,"
            "status,public_date_label,age_limits,has_photo,wiki_page,verified"
        )
        response = self.service.get_groups_by_domains(",".join(domains), fields=fields)

        groups = response["response"]["groups"]

        file_path = groups_path.joinpath("groups.json")
        with open(file_path, "w", encoding=self.encoding) as f:
            json.dump(groups, f, ensure_ascii=False)
