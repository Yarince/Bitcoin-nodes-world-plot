# Python program to check if a given directed graph is strongly
# connected or not
from collections import defaultdict

# This class represents a directed graph using adjacency list representation
from links import priorityDictionary, DistanceCalculator


class Graph:

    def __init__(self):
        self.graph = defaultdict(dict)  # default dictionary to store graph

    # function to add an edge to graph
    def add_edge(self, u, v, distance):
        self.graph[u][v] = distance  # .append({"node": v, "distance": distance})
        self.graph[v][u] = distance  # .append({"node": u, "distance": distance})

    # A function used by isSC() to perform DFS
    def DFSUtil(self, v, visited):

        # Mark the current node as visited
        visited[v] = True

        # Recur for all the vertices adjacent to this vertex
        for i in [x for x in self.graph[v].keys()]:
            if not visited[i]:
                self.DFSUtil(i, visited)

    # Function that returns reverse (or transpose) of this graph
    # Returns true if given graph is
    # connected, else false
    def is_connected(self):
        visited = {node: False for node in self.graph}

        # Find all reachable vertices
        # from first vertex
        if len(self.graph) == 0:
            return False
        # Get the first node in the graph
        v = next(iter(self.graph))
        self.DFSUtil(v, visited)

        # If set of reachable vertices
        # includes all, return true.
        for i in self.graph:
            if not visited[i]:
                return False

        return True

    def printSolution(self, start, dist):
        print("From", start)
        items = [node.__str__() + "\t\t\t\t\t " + str(distance) for node, distance in dist.items()]
        for item in items:
            print(item)
        print("------------------------------------------------------------------")

    # David Eppstein, UC Irvine, 4 April 2002
    def dijkstra(self, start, end=None):
        """
        Find shortest paths from the start vertex to all
        vertices nearer than or equal to the end.

        The input graph G is assumed to have the following
        representation: A vertex can be any object that can
        be used as an index into a dictionary.  G is a
        dictionary, indexed by vertices.  For any vertex v,
        G[v] is itself a dictionary, indexed by the neighbors
        of v.  For any edge v->w, G[v][w] is the length of
        the edge.  This is related to the representation in
        <http://www.python.org/doc/essays/graphs.html>
        where Guido van Rossum suggests representing graphs
        as dictionaries mapping vertices to lists of neighbors,
        however dictionaries of edges have many advantages
        over lists: they can store extra information (here,
        the lengths), they support fast existence tests,
        and they allow easy modification of the graph by edge
        insertion and removal.  Such modifications are not
        needed here but are important in other graph algorithms.
        Since dictionaries obey iterator protocol, a graph
        represented as described here could be handed without
        modification to an algorithm using Guido's representation.

        Of course, G and G[v] need not be Python dict objects;
        they can be any other object that obeys dict protocol,
        for instance a wrapper in which vertices are URLs
        and a call to G[v] loads the web page and finds its links.

        The output is a pair (D,P) where D[v] is the distance
        from start to v and P[v] is the predecessor of v along
        the shortest path from s to v.

        Dijkstra's algorithm is only guaranteed to work correctly
        when all edge lengths are positive. This code does not
        verify this property for all edges (only the edges seen
         before the end vertex is reached), but will correctly
        compute shortest paths even for some graphs with negative
        edges, and will raise an exception if it discovers that
        a negative edge has caused it to make a mistake.
        """

        D = {}  # dictionary of final distances
        P = {}  # dictionary of predecessors
        Q = priorityDictionary()  # est.dist. of non-final vert.
        Q[start] = 0

        for v in Q:
            D[v] = Q[v]
            if v == end:
                break

            for w in self.graph[v]:
                vwLength = D[v] + self.graph[v][w]
                if w in D:
                    if vwLength < D[w]:
                        raise ValueError("Dijkstra: found better path to already-final vertex")
                elif w not in Q or vwLength < Q[w]:
                    Q[w] = vwLength
                    P[w] = v

        return D

    def shortestPath(self, start, end):
        """
        Find a single shortest path from the given start vertex
        to the given end vertex.
        The input has the same conventions as Dijkstra().
        The output is a list of the vertices in order along
        the shortest path.
        """

        D, P = self.dijkstra(start, end)
        Path = []
        while 1:
            Path.append(end)
            if end == start:
                break
            end = P[end]
        Path.reverse()
        return Path

    def add_extra_relays(self, extra_relays):
        self.add_edge(extra_relays[0], extra_relays[1],
                      DistanceCalculator.great_distance_calc(extra_relays[0], extra_relays[1]))
        self.add_edge(extra_relays[1], extra_relays[2],
                      DistanceCalculator.great_distance_calc(extra_relays[1], extra_relays[2]))

# This code is contributed by Neelam Yadav, Divyanshu Mehta and Yarince Martis
