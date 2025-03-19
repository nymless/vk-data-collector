from client.client import Client
from collector.collector import Collector
from service.service import Service


def main():
    client = Client()
    service = Service(client)
    collector = Collector(service)

    collector.collect_all_posts("club51059456")


if __name__ == "__main__":
    main()
