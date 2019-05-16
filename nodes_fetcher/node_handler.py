import os
import random
from collections import defaultdict

from nodes_fetcher import Node, JsonParser


class NodeHandler:

    def __init__(self):
        random_data = os.urandom(4)
        seed = int.from_bytes(random_data, byteorder="big")
        random.seed(seed)

        parser = JsonParser
        # uncomment to refresh node data
        # parser.download_and_write_node_info()
        self.nodes = self.filter_nodes(parser.load_nodes_from_file())

    # Remove nodes with missing crucial data
    def filter_nodes(self, nodes):
        filtered_nodes = []
        for node in nodes:
            if node.host_name is not None and node.city is not None and node.country is not None and \
                    node.latitude is not None and node.longitude is not None:
                filtered_nodes.append(node)
        return filtered_nodes

    @staticmethod
    def group_nodes_by_city_country(nodes):
        # Group nodes by country and then by city
        res = defaultdict(list)
        for v in nodes:
            city_country = v.city + ", " + v.country
            res[city_country].append(v)
        grouped = [{'city_country': k, 'nodes': c} for k, c in res.items()]

        country_res = defaultdict(list)
        for v in [x['nodes'] for x in grouped]:
            country = v[0].country
            country_res[country].append(v)

        # Group all nodes per country and per city
        grouped_country_city = dict(dict())
        for country, items in country_res.items():
            for nodes in items:
                city = nodes[0].city
                for node in nodes:
                    if country not in grouped_country_city:
                        grouped_country_city[country] = {}
                    if city not in grouped_country_city[country]:
                        grouped_country_city[country][city] = {'nodes': []}
                    grouped_country_city[country][city]['nodes'].append(node)

        return grouped_country_city

    @staticmethod
    def print_nodes_per_city(grouped_country_city):
        for country, city_node in grouped_country_city.items():
            for city, nodes in city_node.items():
                if len(city) > 1:
                    print(country + ": " + city + ": " + str(len(nodes['nodes'])))

    @staticmethod
    def get_one_node_per_city(grouped_country_city):
        miner_per_city = dict(dict())

        for country, cities in grouped_country_city.items():
            # random_city = random.choice(list(cities.keys()))
            for random_city, nodes in cities.items():
                if country not in miner_per_city:
                    miner_per_city[country] = {}
                choice = random.choice(list(cities[random_city]['nodes']))
                miner_per_city[country][random_city] = choice

        return miner_per_city

    @staticmethod
    def share(available, members):

        count = 0
        # find across how many members we must distribute and what the total sum of those values is
        total = available
        for idx, member in enumerate(members):
            total += member
            count = idx + 1
            if idx >= len(members) - 1:
                break
            if total / (idx + 1) <= members[idx + 1]:
                break

        # distribute the total value among 'count' first value
        distr = []
        for member in members[0:count]:
            target = total // count
            diff = target - member
            distr.append(diff)

            total -= target
            count -= 1

        return distr

    @staticmethod
    def constrained_sum_sample_pos(n, total):
        """Return a randomly chosen list of n positive integers summing to total.
        Each such list is equally likely to occur."""

        sample = random.sample(range(1, total), n - 1)
        dividers = sorted(sample)
        return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

    def get_nodes(self, miner_per_city, no_nodes, countries):
        nodes = []
        share = self.constrained_sum_sample_pos(len(countries), no_nodes)
        country_iter = countries.__iter__()
        share_iter = share.__iter__()
        country = next(country_iter)
        amount = next(share_iter)
        while True:
            try:
                count = 0

                while count < amount:
                    if country in miner_per_city:
                        if len(miner_per_city[country]) <= 0:
                            remaining = amount - count
                            amount = next(share_iter)
                            amount += remaining
                            break
                        nodes_in_country = miner_per_city[country]
                        node = random.choice(list(nodes_in_country.values()))
                        del miner_per_city[country][node.city]
                        nodes.append(node)
                        count += 1
                if count == amount:
                    amount = next(share_iter)
                country = next(country_iter)
            except StopIteration:
                break
        return nodes

    def get_extra_relays(self):
        grouped = self.group_nodes_by_city_country(self.nodes)
        new_relays = [
            grouped["CN"]["Shanghai"]['nodes'][0],
            Node.create_relay("US", "Kaneohe", 21.454, -157.830),
            Node.create_relay("US", "Oakland", 37.805, -122.212)
        ]

        return new_relays

    def get_selected_nodes(self):
        grouped_country_city = self.group_nodes_by_city_country(self.nodes)

        # Represent every city with maximum 1 node
        miner_per_city = self.get_one_node_per_city(grouped_country_city)

        honest_miners = self.get_nodes(miner_per_city, 10, ["IS", "NO", "CN", "CA"])
        dishonest_miners = self.get_nodes(miner_per_city, 10, ["CN", "CA", "CH", "KZ", "KW"])
        relays = self.get_nodes(miner_per_city, 5, ["RU", "RO"]) + self.get_extra_relays()

        return honest_miners, dishonest_miners, relays
