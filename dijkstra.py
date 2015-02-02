#
# The code below uses a linear
# scan to find the unfinished node
# with the smallest distance from
# the source.
#
# Modify it to use a heap instead
# 

def shortest_dist_node(heap,heap_places):
    best_node = heap[0][1]
    del heap_places[best_node]
    if len(heap) == 1:
        heap.pop()
    else:
        heap[0] = heap.pop()
        heap_places[heap[0][1]] = 0
        down_heapify(heap,0,heap_places)
    return best_node,heap

def dijkstra(G,v):
    dist_so_far = {}
    dist_so_far[v] = 0
    heap = [(0,v)]
    heap_places = {v:0}
    final_dist = {}
    node_predecessor = {}
    while len(heap) !=0:
        w,heap = shortest_dist_node(heap,heap_places)
        # lock it down!
        final_dist[w] = dist_so_far[w]
        del dist_so_far[w]
        for x in G[w]:
            if x not in final_dist:
                if x not in dist_so_far:
                    dist_so_far[x] = final_dist[w] + G[w][x]
                    node_predecessor[x] = w
                    heap.append((dist_so_far[x],x))
                    heap_places[x] = len(heap)-1
                    up_heapify(heap,len(heap)-1,heap_places)
                elif final_dist[w] + G[w][x] < dist_so_far[x]:
                    index = heap_places[x] 
                    dist_so_far[x] = final_dist[w] + G[w][x]
                    node_predecessor[x] = w
                    heap[index] = (dist_so_far[x],x)
                    up_heapify(heap,index,heap_places)
    return final_dist, node_predecessor

############
# 
# Test

def make_link(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 0
    (G[node1])[node2] += w
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 0
    (G[node2])[node1] += w
    return G


def test():
    # shortcuts
    (a,b,c,d,e,f,g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    triples = ((a,c,3),(c,b,10),(a,b,15),(d,b,9),(a,d,4),(d,f,7),(d,e,3), 
               (e,g,1),(e,f,5),(f,g,2),(b,f,1))
    G = {}
    for (i,j,k) in triples:
        make_link(G, i, j, k)

    dist = dijkstra(G, a)
    print dist
    print dist[g] == 8 #(a -> d -> e -> g)
    print dist[b] == 11 #(a -> d -> e -> g -> f -> b)

def down_heapify(L, i,heap_places):
    # If i is a leaf, heap property holds
    if leaf(L, i): return
    # If i has one child...
    if one_child(L, i):
        # check heap property
        if L[i] > L[left(i)]:
            # if it fail, swap, fixing i and its child (a leaf)
            heap_places[L[i][1]],heap_places[L[left(i)][1]] = left(i),i
            (L[i], L[left(i)]) = (L[left(i)], L[i])      
        return
    # if i has two children...
    # check heap property
    if min(L[left(i)], L[right(i)]) >= L[i]: return
    # If it fails, see which child is the smaller
    # and swap i's value into that child
    # Afterwards, recurse into that child, which might violate
    if L[left(i)] < L[right(i)]:
        # Swap into left child
        heap_places[L[i][1]],heap_places[L[left(i)][1]] = left(i),i
        (L[i], L[left(i)]) = (L[left(i)], L[i]) 
        down_heapify(L, left(i),heap_places)
        return
    heap_places[L[i][1]],heap_places[L[right(i)][1]] = right(i),i
    (L[i], L[right(i)]) = (L[right(i)], L[i])
    down_heapify(L, right(i),heap_places)
    return

def up_heapify(L, i,heap_places):
    if i == 0 or L[parent(i)] <= L[i]:
        return
    heap_places[L[i][1]],heap_places[L[parent(i)][1]] = parent(i),i
    L[parent(i)],L[i] = L[i], L[parent(i)]  
    return up_heapify(L,parent(i),heap_places)
        
def parent(i): 
    return (i-1)/2
def left(i): 
    return 2*i+1
def right(i): 
    return 2*i+2
def leaf(L,i): 
    return (left(i) >= len(L)) and (right(i) >= len(L))
def one_child(L,i): 
    return (left(i) < len(L)) and (right(i) >= len(L))

#test()
