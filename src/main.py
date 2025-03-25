from client.client import Client
from collector.collector import Collector
from service.service import Service


def main():
    client = Client()
    service = Service(client)
    collector = Collector(service)

    depression_groups = ["club51059456"]
    control_groups = ["mshsrf", "artandtoysgroup", "mamkrasnodar"]

    depression_files = ["data/posts/depression/club51059456_posts.json"]
    control_files = [
        "data/posts/control/artandtoysgroup_posts.json",
        "data/posts/control/mamkrasnodar_posts.json",
        "data/posts/control/mshsrf_posts.json",
    ]

    collector.collect_all_posts(depression_groups, "data/posts/depression")
    collector.collect_all_posts(control_groups, "data/posts/control")

    collector.collect_groups(depression_groups, "data/groups/depression")
    collector.collect_groups(control_groups, "data/groups/control")

    collector.collect_comments_for_posts(depression_files, "data/comments/depression")
    collector.collect_comments_for_posts(control_files, "data/comments/control")


if __name__ == "__main__":
    main()
