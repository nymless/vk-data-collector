from client.client import Client
from collector.collector import Collector
from service.service import Service


def main():
    client = Client()
    service = Service(client)
    collector = Collector(service)

    # collector.collect_all_posts("club51059456", "data/raw/depression/posts")

    control_groups = ["mshsrf", "artandtoysgroup", "mamkrasnodar"]
    collector.collect_all_posts(control_groups, "data/raw/control/posts")


if __name__ == "__main__":
    main()
