import os

import requests
from dotenv import load_dotenv

load_dotenv()


class Client:
    base_url = "https://api.vk.com"

    _user_token = ""

    def __init__(self):
        self.service_token = os.getenv("SERVICE_TOKEN")

    def make_request(self, endpoint, params, v="5.199"):
        url = self.base_url + endpoint
        params["access_token"] = self.service_token
        params["v"] = v
        response = requests.get(url, params=params)
        return response
