from client.client import Client
from collector.collector import Collector
from service.service import Service


def main():
    client = Client()
    service = Service(client)
    collector = Collector(service)

    depression_groups = ["club51059456"]
    control_groups = ["mshsrf", "artandtoysgroup", "mamkrasnodar"]

    collector.collect_all_posts(depression_groups, "data/posts/depression")
    collector.collect_all_posts(control_groups, "data/posts/control")
    collector.collect_groups(depression_groups, "data/groups/depression")
    collector.collect_groups(control_groups, "data/groups/control")


if __name__ == "__main__":
    main()
