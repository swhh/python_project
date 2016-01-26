#  
# This is the same problem as "Distance Oracle I" except that instead of
# only having to deal with binary trees, the assignment asks you to
# create labels for all tree graphs.
#
# In the shortest-path oracle described in Andrew Goldberg's
# interview, each node has a label, which is a list of some other
# nodes in the network and their distance to these nodes.  These lists
# have the property that
#
#  (1) for any pair of nodes (x,y) in the network, their lists will
#  have at least one node z in common
#
#  (2) the shortest path from x to y will go through z.
# 
# Given a graph G that is a tree, preprocess the graph to
# create such labels for each node.  Note that the size of the list in
# each label should not be larger than log n for a graph of size n.
#

#
# create_labels takes in a tree and returns a dictionary, mapping each
# node to its label
#
# a label is a dictionary mapping another node and the distance to
# that node
#
from collections import defaultdict
import math


def centrality(G,v):
   """return max distance between node v and any other node in G"""
   return max([distance(G,v,v1) for v1 in G.keys() if v1 != v])

def find_root(G):
   """return root where root is node in G with minimum max distance to any other node"""
   return min(G.keys(),key=lambda x: centrality(G,x))
   
def remove_node(G,node):
   """return new disconnected graph with 'node' removed"""
   new_G = G.copy()
   for neighbor in G[node].keys():
      del new_G[neighbor][node]
   del new_G[node]
   return new_G
   
def mark_component(G, node, marked):
    """recursively find all nodes connected to 'node'"""
    marked[node] = True
    for neighbor in G[node]:
        if neighbor not in marked:
            mark_component(G, neighbor, marked)
    return marked.keys()

def split_graph(G,root):
   """remove root from graph and return subtrees created by removal"""
   new_G = remove_node(G,root)
   subtrees = []
   for neighbor in G[root]:
      nodes = mark_component(new_G,neighbor,{})
      subtree = {node:new_G[node] for node in nodes}
      subtrees.append(subtree)
   return subtrees
        

def create_labels(G):
    """build dictionary of labels for G with no label larger than log n where n is size of G"""
    labels = defaultdict(dict)
    for node in G:
       labels[node][node] = 0
    recurse_labels(G,G.keys(),labels)
    return labels
                

def recurse_labels(G,chain,labels):
   """Assign labels to nodes finding the root of G, splitting into subtrees and then recurse"""
   if len(chain) == 2:
      a,b = chain[0],chain[1]
      labels[a][b] = distance(G,a,b)
      return labels
   if len(chain) == 1:
      return labels
   root = find_root(G)
   for node in G.keys():
      labels[node][root] = distance(G,node,root)
   subtrees = split_graph(G,root)
   for subtree in subtrees:
      recurse_labels(subtree,subtree.keys(),labels)
   return labels

   


#######
# Testing
#


def get_distances(G, labels):
    # labels = {a:{b: distance from a to b,
    #              c: distance from a to c}}
    # create a mapping of all distances for
    # all nodes
    distances = {}
    for start in G:
        # get all the labels for my starting node
        label_node = labels[start]
        s_distances = {}
        for destination in G:
            shortest = float('inf')
            # get all the labels for the destination node
            label_dest = labels[destination]
            # and then merge them together, saving the
            # shortest distance
            for intermediate_node, dist in label_node.iteritems():
                # see if intermediate_node is our destination
                # if it is we can stop - we know that is
                # the shortest path
                if intermediate_node == destination:
                    shortest = dist
                    break
                other_dist = label_dest.get(intermediate_node)
                if other_dist is None:
                    continue
                if other_dist + dist < shortest:
                    shortest = other_dist + dist
            s_distances[destination] = shortest
        distances[start] = s_distances
    return distances

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G
    
    
def path(G, v1, v2):
    #distance_from_start = {}
    path_from_start = {} # modification
    open_list = [v1]
    #distance_from_start[v1] = 0
    path_from_start[v1] = [v1] # modification
    while len(open_list) > 0:
        current = open_list[0]
        del open_list[0]
        for neighbor in G[current].keys():
            #if neighbor not in distance_from_start:
            if neighbor not in path_from_start: # modification
                #distance_from_start[neighbor] = distance_from_start[current] + 1
                path_from_start[neighbor] = path_from_start[current] + [neighbor] # modification
                #if neighbor == v2: return distance_from_start[v2]
                if neighbor == v2: return path_from_start[v2] # modification
                open_list.append(neighbor)
    return False

def distance(G, v1, v2):
    if v1 == v2:
       return 0
    distance_from_start = {}
    open_list = [v1]
    distance_from_start[v1] = 0
    while len(open_list) > 0:
        current = open_list[0]
        del open_list[0]
        for neighbor in G[current].keys():
            if neighbor not in distance_from_start:
                distance_from_start[neighbor] = distance_from_start[current] + G[current][neighbor]
                if neighbor == v2: return distance_from_start[v2]
                open_list.append(neighbor)
    return False


def max_labels(labels):
    return max(len(labels[u]) for u in labels)

def labels_needed(G):
    return 1 + int(math.ceil(math.log(len(G))/math.log(2)))


def test():
    # binary tree
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
             (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree)
    assert labels_needed(tree) >= max_labels(labels)
    distances = get_distances(tree, labels)
    assert distances[1][2] == 1
    assert distances[1][4] == 2    
    assert distances[4][1] == 2
    assert distances[1][4] == 2
    assert distances[2][1] == 1
    assert distances[1][2] == 1   
    assert distances[1][1] == 0
    assert distances[2][2] == 0
    assert distances[9][9] == 0
    assert distances[2][3] == 2
    assert distances[12][13] == 2
    assert distances[13][8] == 6
    assert distances[11][12] == 6
    assert distances[1][12] == 3
    print 'test1 passes'

    # chain graph
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7),
             (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree)
    assert labels_needed(tree) >= max_labels(labels)
    distances = get_distances(tree, labels)
    assert distances[1][2] == 1
    assert distances[1][3] == 2
    assert distances[1][13] == 12
    assert distances[6][1] == 5
    assert distances[6][13] == 7
    assert distances[8][3] == 5
    assert distances[10][4] == 6
    print 'test2 passes'

    # "star-chain" graph
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (1, 6), (6, 7), 
             (7, 8), (8, 9), (1, 10), (10, 11), (11, 12), (12, 13)]    
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree)
    assert labels_needed(tree) >= max_labels(labels)
    distances = get_distances(tree, labels)
    assert distances[1][1] == 0
    assert distances[5][5] == 0
    assert distances[1][2] == 1
    assert distances[1][3] == 2    
    assert distances[1][4] == 3
    assert distances[1][5] == 4
    assert distances[5][6] == 5
    assert distances[5][7] == 6
    assert distances[5][8] == 7
    assert distances[5][9] == 8
    print 'test3 passes'

test()

