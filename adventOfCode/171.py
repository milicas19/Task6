import heapq
from collections import deque
import sys
DIR = [(0, 1), (0, -1), (1, 0), (-1, 0)]
# iPair ==> Integer Pair
iPair = tuple
def valid(pos, dir, valid_dict, n, m):
    (i, j) = pos
    (i_dir, j_dir) = dir
    
    #if i + 3*i_dir < n and i + 3*i_dir >= 0 and j + 3*j_dir < m and j + 3*j_dir >= 0 and (i + i_dir, j + j_dir) in valid_dict[pos] and (i + 2*i_dir, j + 2*j_dir) in valid_dict[pos] and (i + 3*i_dir, j + 3*j_dir) in valid_dict[pos]:
        #return False
    if i - 3*i_dir < n and i - 3*i_dir >= 0 and j - 3*j_dir < m and j - 3*j_dir >= 0 and (i - i_dir, j - j_dir) in valid_dict[dir] and (i - 2*i_dir, j - 2*j_dir) in valid_dict[dir] and (i - 3*i_dir, j - 3*j_dir) in valid_dict[dir]:
        return False
    return True

def get_neighbors(pos, pdir, n, m, valid_dict):
    (i, j) = pos
    neighbors = set()
    if pdir == (0, 1):
        skip = (0, -1)
    elif pdir == (1, 0):
        skip = (-1, 0)
    elif pdir == (0, -1):
        skip = (0, 1)
    elif pdir == (-1, 0):
        skip = (1, 0)
    
    for dir in DIR:
        if dir == skip:
            continue
        (i_dir, j_dir) = dir
        new_pos = (i + i_dir, j + j_dir)
        if i + i_dir >= 0 and i + i_dir < n and j + j_dir >= 0 and j + j_dir < m and valid(new_pos, dir, valid_dict, n, m):
            valid_dict[dir].add(new_pos)
            neighbors.add((new_pos, dir))
    
    return neighbors
# This class represents a directed graph using
# adjacency list representation
class Graph:
	def __init__(self, V: int): # Constructor
		self.V = V
		self.adj = [[] for _ in range(V)]

	def addEdge(self, u: int, v: int, w: int):
		self.adj[u].append((v, w))
		self.adj[v].append((u, w))

	# Prints shortest paths from src to all other vertices
	def shortestPath(self, src: int):
		# Create a priority queue to store vertices that
		# are being preprocessed
		pq = []
		heapq.heappush(pq, (0, src))

		# Create a vector for distances and initialize all
		# distances as infinite (INF)
		dist = [float('inf')] * self.V
		dist[src] = 0

		while pq:
			# The first vertex in pair is the minimum distance
			# vertex, extract it from priority queue.
			# vertex label is stored in second of pair
			d, u = heapq.heappop(pq)

			# 'i' is used to get all adjacent vertices of a
			# vertex
			for v, weight in self.adj[u]:
				# If there is shorted path to v through u.
				if dist[v] > dist[u] + weight:
					# Updating distance of v
					dist[v] = dist[u] + weight
					heapq.heappush(pq, (dist[v], v))

		# Print shortest distances stored in dist[]
		for i in range(self.V):
			print(f"{i} \t\t {dist[i]}")

# Driver's code
if __name__ == "__main__":
    
    matrix = []
    file_name = 'input171.txt'
    
    with open(file_name, 'r') as file:
        inputs = []
        for line in file:
            row_num = []
            row = line.strip()
            for num_str in row:
                row_num.append(int(num_str))
            matrix.append(row_num)
    
    n = len(matrix)
    m = len(matrix[0])
    
    curr_pos = (0, 0)
    curr_dir = (0, 1)
    
    valid_dict = dict()
    for dir in DIR:
        valid_dict[dir] = set([curr_pos])
        
    edges = []
    nodes = deque()
    nodes.append((curr_pos, curr_dir))
    V = 0
    visited = dict()
    
    while nodes:
        (curr_pos, curr_dir) = nodes.popleft()
        if (curr_pos, curr_dir) in visited:
            continue
        visited[(curr_pos, curr_dir)] = 1
        print(curr_pos)
        V += 1
        (i, j) = curr_pos
        neighbors = get_neighbors(curr_pos, curr_dir, n, m, valid_dict)
        print(f"pos = {curr_pos} neigh = {neighbors}")
        for (n_i, n_j), n_dir in neighbors:
            if ((n_i, n_j), n_dir) not in visited:
                nodes.append(((n_i, n_j), n_dir))
                edge = (i * m + j, n_i * m + n_j, matrix[n_i][n_j])
                edges.append(edge)

    #print(edges)
    #g = Graph(V)
    #for (curr, next, dist) in edges:
        #g.addEdge(curr, next, dist)
    #g.shortestPath(0)
