import random

def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:            
            memo[x] = f(x)
        return memo[x]
    return helper

def graph(file):
   G = {}
   actors = set()
   for line in file.readlines():
       values = line.split('\t')
       name,movie = values[0],(values[1],values[2])
       make_link(G,name,movie)
       actors.add(name)
   return G,actors

@memoize
def centrality(v):
    global G
    distance_from_start = {}
    open_list = [v]
    distance_from_start[v] = 0
    while len(open_list) > 0:
        current = open_list[0]
        del open_list[0]
        for neighbor in G[current].keys():
            if neighbor not in distance_from_start:
                distance_from_start[neighbor] = distance_from_start[current] + 1
                open_list.append(neighbor)
    return float(sum(distance_from_start.values()))/len(distance_from_start)


def partition(L, v):
    smaller = []
    bigger = []
    for val in L:
        if centrality(val) < centrality(v): smaller += [val]
        if centrality(val) > centrality(v): bigger += [val]
    return (smaller, [v], bigger)


def top_k(L, k):
    v = L[random.randrange(len(L))]
    (left, middle, right) = partition(L, v)
    # middle used below (in place of [v]) for clarity
    if len(left) == k:   return left
    if len(left)+1 == k: return left + middle
    if len(left) > k:    return top_k(left, k)
    return left + middle + top_k(right, k - len(left) - len(middle))


def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G     


def top_k_actors(number):
   return top_k(actors,number)

def kth_actor(number):
   return min(top_k_actors(number),key=centrality) 

file = open('actors.tsv','r')
G,actors = graph(file)
actors = list(actors)
print top_k_actors(20)
