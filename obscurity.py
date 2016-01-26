import dijkstra
import csv


def read_graph(filename):
    # Read an undirected graph in CSV format. Each line is an edge
    tsv = csv.reader(open(filename), delimiter='\t')
    G = {}
    for (actor, movie,date) in tsv: 
       make_link(G, actor, (movie,date))
    return G

def movie_scores(filename):
   scores = {}
   tsv = csv.reader(open(filename), delimiter='\t')
   for movie,date,score in tsv:
      scores[(movie,date)] = float(score)
   return scores

def movie_obscurity(movie):
   return movie_obscurity_scores[movie]


def make_link(G, actor, movie):
    if actor not in G:
        G[actor] = {}
    (G[actor])[movie] = movie_obscurity(movie)
    if movie not in G:
        G[movie] = {}
    (G[movie])[actor] = movie_obscurity(movie)
    return G 

def weighted_path_finder(node_predecessor,from_node,to_node):
   current = to_node
   path = []
   while current in node_predecessor.keys():
      path.insert(0,current)
      current = node_predecessor[current]
   path.insert(0,from_node)
   return path

def obscurity(dict):
   new_answer = {}
   for actor1,actor2 in dict.keys():
      __, predecessors = dijkstra.dijkstra(G,actor1)
      path = weighted_path_finder(predecessors,actor1,actor2)
      new_answer[(actor1,actor2)] = max([movie_obscurity(movie) for movie in path[1::2]])
   return new_answer

movie_obscurity_scores = movie_scores('imdb-weights.tsv')
G = read_graph('imdb.tsv')
answer = {(u'Boone Junior, Mark', u'Del Toro, Benicio'): None,
          (u'Braine, Richard', u'Coogan, Will'): None,
          (u'Byrne, Michael (I)', u'Quinn, Al (I)'): None,
          (u'Cartwright, Veronica', u'Edelstein, Lisa'): None,
          (u'Curry, Jon (II)', u'Wise, Ray (I)'): None,
          (u'Di Benedetto, John', u'Hallgrey, Johnathan'): None,
          (u'Hochendoner, Jeff', u'Cross, Kendall'): None,
          (u'Izquierdo, Ty', u'Kimball, Donna'): None,
          (u'Jace, Michael', u'Snell, Don'): None,
          (u'James, Charity', u'Tuerpe, Paul'): None,
          (u'Kay, Dominic Scott', u'Cathey, Reg E.'): None,
          (u'McCabe, Richard', u'Washington, Denzel'): None,
          (u'Reid, Kevin (I)', u'Affleck, Rab'): None,
          (u'Reid, R.D.', u'Boston, David (IV)'): None,
          (u'Restivo, Steve', u'Preston, Carrie (I)'): None,
          (u'Rodriguez, Ramon (II)', u'Mulrooney, Kelsey'): None,
          (u'Rooker, Michael (I)', u'Grady, Kevin (I)'): None,
          (u'Ruscoe, Alan', u'Thornton, Cooper'): None,
          (u'Sloan, Tina', u'Dever, James D.'): None,
          (u'Wasserman, Jerry', u'Sizemore, Tom'): None}

print obscurity(answer)

   