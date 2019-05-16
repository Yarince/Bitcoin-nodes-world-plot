class Node:
    def __init__(self, ip_port: str or None, number_of_full_nodes: int or None, version: str or None,
                 connected_since: int or None, user_agent: str or None, height_of_blockchain: str or None,
                 host_name: str or None, city: str, country: str, latitude: float, longitude: float,
                 timezone: str or None, ASN: str or None, organisation_name: str or None):
        self.ip_port: str = ip_port
        self.number_of_full_nodes: int = number_of_full_nodes
        self.version: str = version
        self.connected_since: int = connected_since
        self.user_agent: str = user_agent
        self.height_of_blockchain: str = height_of_blockchain
        self.host_name: str = host_name
        self.city: str = city
        self.country: str = country
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.timezone: str = timezone
        self.ASN: str = ASN
        self.organisation_name: str = organisation_name

    @staticmethod
    def create_node(node):
        return Node(
            # ip,
            node[0],
            node[1],
            node[2],
            node[3],
            node[4],
            node[5],
            node[6],
            node[7],
            node[8],
            node[9],
            node[10],
            node[11],
            node[12],
            node[13]
        )

    @staticmethod
    def create_relay(country, city, latitude, longitude):
        return Node(None, None, None, None, None, None, None, city, country, latitude, longitude, None, None, None)

    def __eq__(self, o: object) -> bool:
        if o is None:
            return False
        if not isinstance(o, self.__class__):
            return False

        o: Node
        return o.city == self.city and o.country == self.country

    def __hash__(self) -> int:
        return hash(self.city) ^ hash(self.country)

    def __str__(self) -> str:
        return "Node " + self.country + ": " + self.city + " - " + str(self.latitude) + ", " + str(self.longitude)
        # return f"Node(None, None, None, None, None, None, None, " \
        #     f"{self.city, self.country, self.latitude, self.longitude}, None, None, None)"
