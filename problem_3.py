import random
from sys import argv, exit
from collections import namedtuple, defaultdict

Graph = namedtuple('Graph', ['V', 'E'])


def random_contraction_algorithm(graph):
    n = len(graph.V)
    new_graph = graph
    while n > 2:
        edge = random_select(new_graph)
        new_graph = merge(graph, edge)
        n -= 1
    return new_graph


def random_select(graph):
    edges = graph.E
    edge = random.choice(edges.keys())
    return edge


def merge(graph, edge):
    edges, nodes = graph.E, graph.V
    u, v = edges[edge]
    del edges[edge]
    edges, nodes = transfer(u, v, edges, nodes)
    del nodes[u]
    return Graph(nodes, edges)


def transfer(u, v, edges, nodes):
    for edge in [edge for edge in nodes[u] if edges.get(edge)]:
        edge_nodes = edges[edge]
        if edge_nodes[0] == u:
            edge_nodes[0] = v
        else:
            edge_nodes[1] = v
        if edge_nodes[0] == v and edge_nodes[1] == v:
            del edges[edge]
        else:
            nodes[v].append(edge)
    return edges, nodes


if __name__ == '__main__':
    f = argv[1]
    V = defaultdict(list)
    E = dict()
    edge_num = 1
    with open(f) as f:
        for line in f:
            vertices = map(int, line.split())
            vertex, neighbors = vertices[0], vertices[1:]
            for neighbor in neighbors:
                if vertex < neighbor:
                    E[edge_num] = [vertex, neighbor]
                    V[vertex].append(edge_num)
                    V[neighbor].append(edge_num)
                    edge_num += 1
    graph = Graph(V, E)
    new_graph = random_contraction_algorithm(graph)







