from client.client import Client
from collector.collector import Collector
from service.service import Service


def main():
    client = Client()
    service = Service(client)
    collector = Collector(service)

    depression_groups = ["club51059456"]
    control_groups = ["mshsrf", "artandtoysgroup", "mamkrasnodar"]

    def get_posts():
        collector.collect_all_posts(depression_groups, "data/posts/depression")
        collector.collect_all_posts(control_groups, "data/posts/control")

    def get_groups():
        collector.collect_groups(depression_groups, "data/groups/depression")
        collector.collect_groups(control_groups, "data/groups/control")

    def get_missing_comments():
        collector.collect_comments_for_posts(
            "data/posts/depression/club51059456_posts.json",
            "data/comments/depression",
        )
        collector.collect_comments_for_posts(
            "data/posts/control/artandtoysgroup_posts.json",
            "data/comments/control",
        )
        collector.collect_comments_for_posts(
            "data/posts/control/mamkrasnodar_posts.json",
            "data/comments/control",
        )
        collector.collect_comments_for_posts(
            "data/posts/control/mshsrf_posts.json",
            "data/comments/control",
        )

    # get_posts()
    # get_groups()
    get_missing_comments()


if __name__ == "__main__":
    main()
