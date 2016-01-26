from collections import defaultdict, Counter, deque
from sys import argv, setrecursionlimit


setrecursionlimit(10**6)


def strongly_connected_components(graph, graph_size):
    strongly_connected_components.order = deque()
    strongly_connected_components.components = [None] * (graph_size + 1)
    strongly_connected_components.comp = 0

    def dfs_loop(graph, second_run=False):
        explored = [False] * (graph_size + 1)
        if not second_run:
            nodes = xrange(1, graph_size + 1)
        else:
            nodes = strongly_connected_components.order
        for node in nodes:
            if not explored[node]:
                dfs(graph, node, explored, second_run=second_run)
                strongly_connected_components.comp += 1

    def dfs(graph, s, explored, second_run=False):
        explored[s] = True
        for neighbor in graph[s]:
            if not explored[neighbor]:
                dfs(graph, neighbor, explored, second_run=second_run)
        if not second_run:
            strongly_connected_components.order.appendleft(s)
        else:
            strongly_connected_components.components[s] = strongly_connected_components.comp

    reversed_graph = reverse_graph(graph)
    dfs_loop(reversed_graph)
    dfs_loop(graph, second_run=True)
    return strongly_connected_components.components


def reverse_graph(graph):
    reversed_graph = defaultdict(list)
    for node in graph.iterkeys():
        for neighbor in graph[node]:
            reversed_graph[neighbor].append(node)
    return reversed_graph


if __name__ == '__main__':
    f = argv[1]
    graph = defaultdict(list)
    graph_size = 0
    with open(f) as f:
        for line in f:
            vertex, neighbor = map(int, line.split())
            if vertex > graph_size:
                graph_size = vertex
            if neighbor > graph_size:
                graph_size = neighbor
            graph[vertex].append(neighbor)
    components = strongly_connected_components(graph, graph_size)
    print Counter(components).most_common(5)









