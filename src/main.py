from client.client import Client
from collector.collector import Collector
from service.service import Service


def main():
    client = Client()
    service = Service(client)
    collector = Collector(service)

    depression_groups = ["club51059456"]
    control_groups = ["mshsrf", "artandtoysgroup", "mamkrasnodar"]

    collector.collect_all_posts(depression_groups, "data/raw/posts/depression")
    collector.collect_all_posts(control_groups, "data/raw/posts/control")
    collector.collect_groups(",".join(depression_groups), "data/raw/groups/depression")
    collector.collect_groups(",".join(control_groups), "data/raw/groups/control")


if __name__ == "__main__":
    main()
