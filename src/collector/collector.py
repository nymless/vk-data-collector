import json
import sys
from pathlib import Path

from service.service import Service


class Collector:
    def __init__(self, service: Service):
        self.service = service

    def collect_all_posts(self, domain):
        response = self.service.get_wall_posts_by_domain(domain, count=1)

        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        encoding = sys.getdefaultencoding()

        count = response["response"]["count"]
        offset = 100
        runs = (count + offset - 1) // offset

        for i in range(runs):
            response = self.service.get_wall_posts_by_domain(
                domain, count=100, offset=offset * i
            )
            items = response["response"]["items"]

            with open(f"data/posts_{i}.json", "w", encoding=encoding) as f:
                json.dump(items, f, ensure_ascii=False)

        with open("data/posts.json", "w", encoding=encoding) as f:
            posts = []
            for i in range(runs):
                with open(f"data/posts_{i}.json", "r", encoding=encoding) as fp:
                    items = json.load(fp)
                    posts.extend(items)
            json.dump(posts, f, ensure_ascii=False)
