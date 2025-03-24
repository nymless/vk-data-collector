import json
import os
import sys
from pathlib import Path

from lib.types.objects.comment import Comment
from service.service import Service


class Collector:
    def __init__(self, service: Service):
        self.service = service
        self.encoding = sys.getdefaultencoding()

    def _process_path(self, path: str) -> Path:
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def collect_all_posts(self, domains: list[str], path: str) -> None:
        """Collect all posts from the specified VK domains (screen names)
        and save them to JSON files.
        """
        for domain in domains:
            posts_path = self._process_path(path)

            response = self.service.get_wall_posts_by_domain(domain, count=1)

            count = response["response"]["count"]
            chunk_size = 100
            runs = (count + chunk_size - 1) // chunk_size

            for i in range(runs):
                response = self.service.get_wall_posts_by_domain(
                    domain, count=chunk_size, offset=chunk_size * i
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

    def collect_groups(self, domains: list[str], path: str) -> None:
        groups_path = self._process_path(path)

        fields = (
            "activity,wall,city,description,cover,members_count,place,site,"
            "status,public_date_label,age_limits,has_photo,wiki_page,verified"
        )
        response = self.service.get_groups_by_domains(
            ",".join(domains),
            fields=fields,
        )

        groups = response["response"]["groups"]

        file_path = groups_path.joinpath("groups.json")
        with open(file_path, "w", encoding=self.encoding) as f:
            json.dump(groups, f, ensure_ascii=False)

    def collect_comments(self, owner_id: int, post_id: int) -> list[Comment]:
        """Collect all post comments along with their nested threads."""

        chunk_size = 100

        first_res = self.service.get_comments_by_wall_post(
            owner_id=owner_id,
            post_id=post_id,
            count=chunk_size,
            thread_items_count=10,
        )
        response = first_res["response"]

        top_level_count = response["current_level_count"]
        top_level_comments = response["items"]
        top_level_received = len(top_level_comments)

        while top_level_received < top_level_count:
            next_res = self.service.get_comments_by_wall_post(
                owner_id=owner_id,
                post_id=post_id,
                count=chunk_size,
                offset=top_level_received,
                thread_items_count=10,
            )
            items = next_res["response"]["items"]
            top_level_comments.extend(items)
            top_level_received += len(items)

            if len(items) < chunk_size:
                break

        for comment in top_level_comments:
            thread = comment["thread"]
            thread_level_count = thread["count"]

            if thread_level_count <= 10:
                continue

            thread_level_comments = thread["items"]
            thread_level_received = len(thread_level_comments)

            while thread_level_received < thread_level_count:
                thread_res = self.service.get_thread_by_comment(
                    owner_id=owner_id,
                    post_id=post_id,
                    comment_id=comment["id"],
                    count=chunk_size,
                    offset=thread_level_received,
                )
                thread_items = thread_res["response"]["items"]
                thread_level_comments.extend(thread_items)
                thread_level_received += len(thread_items)

                if len(thread_items) < chunk_size:
                    break

        return top_level_comments

    def collect_comments_for_posts(self, posts_file_path: str, path: str) -> None:
        """Collect comments for previously collected wall posts,
        saved to a file.
        """
        comments_path = self._process_path(path)

        with open(posts_file_path, "r", encoding=self.encoding) as f:
            posts = json.load(f)

        comments_dict = {}

        for post in posts:
            if post["comments"]["count"] == 0:
                continue

            post_comments = self.collect_comments(post["owner_id"], post["id"])

            key = f"{post['owner_id']}_{post['id']}"
            comments_dict[key] = post_comments

        p = Path(posts_file_path)
        output_filename = p.stem + "_comments.json"
        comments_file_path = comments_path.joinpath(output_filename)

        with open(comments_file_path, "w", encoding=self.encoding) as f:
            json.dump(comments_dict, f, ensure_ascii=False)
