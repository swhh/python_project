import csv
import dijkstra

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G 

def get_characters(filename):
    tsv = csv.reader(open(filename), delimiter='\t')
    characters = set()
    for (char,comic) in tsv:
       characters.add(char)
    return characters

def read_graph(filename):
    # Read an undirected graph in CSV format. Each line is an edge
    tsv = csv.reader(open(filename), delimiter='\t')
    G = {}
    for (node1, node2) in tsv: 
       make_link(G, node1, node2)
    return G

# Read the marvel comics graph
marvelG = read_graph('file.tsv')


def weight_characters_graph(filename):
    characters = get_characters(filename)
    G = {}
    for char1 in characters:
       for book in marvelG[char1]:
          for char2 in marvelG[book]:
             if char1 > char2:
                dijkstra.make_link(G,char1,char2,1)
    return G

# path from start (after modification on distance())
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

      
def weighted_path_finder(node_predecessor,from_node,to_node):
   current = to_node
   path = []
   while current in node_predecessor.keys():
      path.insert(0,current)
      current = node_predecessor[current]
   path.insert(0,from_node)
   return path
   


def path_differences(node_list):
   count = 0
   for node in node_list:
      weighted_paths,node_predecessor = dijkstra.dijkstra(weight_marvelG,node)
      for char in weighted_paths.keys():
         naive_path = path(weight_marvelG,node,char)
         weighted_path = weighted_path_finder(node_predecessor,node,char)
         if naive_path:
            if len(naive_path) != len(weighted_path):
               count+=1
   return count


node_list = ['SPIDER-MAN/PETER PAR','GREEN GOBLIN/NORMAN ', 'WOLVERINE/LOGAN ','PROFESSOR X/CHARLES ','CAPTAIN AMERICA']
weight_marvelG = weight_characters_graph('file.tsv')
weight_marvelG = {key:{char2:(1.0/count) for char2,count in value.items()} for key,value in weight_marvelG.items()}
print path_differences(node_list)


      


   
   
   

