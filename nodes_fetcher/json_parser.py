import json
import os
import random
from collections import defaultdict

import requests

from nodes_fetcher.node import Node


class JsonParser:

    @staticmethod
    def download_and_write_node_info():
        url_for_stamps = "https://bitnodes.earn.com/api/v1/snapshots/?limit=1"
        timestamp_data = json.loads(requests.get(url_for_stamps).text)
        data = json.loads(
            requests.get(
                "https://bitnodes.earn.com/api/v1/snapshots/" + str(
                    timestamp_data["results"][0]["timestamp"]) + "/").text)

        # Write to file
        f = open("../reachableNodes.json2", "w")
        f.write(json.dumps(data, indent=4))
        f.close()

    @staticmethod
    def load_nodes_from_file():
        nodes = []
        f = open("../reachableNodes.json", "r")
        # f = open("smallNodes.json", "r")
        data = json.loads(f.read())
        f.close()
        for x, y in data['nodes'].items():
            # y = y.append(x)
            nodes.append(Node.create_node([x] + y))
        return nodes
