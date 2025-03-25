from client.client import Client
from collector.collector import Collector
from service.service import Service


def main():
    client = Client()
    service = Service(client)
    collector = Collector(service)

    vk_groups = ["adepra"]

    collector.collect_groups(vk_groups, "data/groups/depression")
    saved_post_files = collector.collect_all_posts(vk_groups, "data/posts/depression")
    collector.collect_comments_for_posts(saved_post_files, "data/comments/depression")


if __name__ == "__main__":
    main()
