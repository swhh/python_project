import heapq
from collections import defaultdict
from sys import argv


def dijkstra(graph, source):
    distance_so_far = defaultdict(lambda: float('inf'))
    final_distance = dict()
    heap = [(0, source)]
    distance_so_far[source] = 0
    seen = {1}
    while len(heap) > 0:
        distance, smallest = heapq.heappop(heap)
        final_distance[smallest] = distance
        for neighbor in graph[smallest]:
            new_dist = distance + graph[smallest][neighbor]
            if new_dist < distance_so_far[neighbor]:
                distance_so_far[neighbor] = new_dist
                heapq.heapify(heap)
            if neighbor not in seen:
                seen.add(neighbor)
                heapq.heappush(heap, (distance_so_far[neighbor], neighbor))

    return final_distance


if __name__ == '__main__':
    f = argv[1]
    graph = defaultdict(dict)
    with open(f) as f:
        for line in f:
            data = line.split()
            node, edges = int(data[0]), data[1:]
            for edge in edges:
                neighbor, distance = map(int, edge.split(','))
                graph[node][neighbor] = distance
    distances = dijkstra(graph, 1)
    final_nodes = '7,37,59,82,99,115,133,165,188,197'
    print map(lambda x: distances[x], map(int, final_nodes.split(',')))



