import sys
DIR = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def valid(pos, dir, valid_dict, n, m):
    (i, j) = pos
    (i_dir, j_dir) = dir
    
    #if i + 3*i_dir < n and i + 3*i_dir >= 0 and j + 3*j_dir < m and j + 3*j_dir >= 0 and (i + i_dir, j + j_dir) in valid_dict[pos] and (i + 2*i_dir, j + 2*j_dir) in valid_dict[pos] and (i + 3*i_dir, j + 3*j_dir) in valid_dict[pos]:
        #return False
    if i - 3*i_dir < n and i - 3*i_dir >= 0 and j - 3*j_dir < m and j - 3*j_dir >= 0 and (i - i_dir, j - j_dir) in valid_dict[dir] and (i - 2*i_dir, j - 2*j_dir) in valid_dict[dir] and (i - 3*i_dir, j - 3*j_dir) in valid_dict[dir]:
        return False
    return True

def valid_v(pos, dir, dist, n, m):
    (i, j) = pos
    (i_dir, j_dir) = dir
    
    print(f"pos = {pos} dir = {dir}")
    prev = (i - i_dir, j - j_dir)
    (i_prev, j_prev) = prev
    
    if i_prev < 0 or i_prev >= n or j_prev < 0 or j_prev >=m:
        return True
    
    if dir == (0, 1):
        prev = (i - i_dir, j - j_dir)
        (i_prev, j_prev) = prev
        if i_prev - 1 >= 0 and j_prev  >= 0 and dist[i_prev * m + j_prev - 0][0] ==  dist[(i_prev - 1) * m + j_prev][0] + matrix[i_prev][j_prev]:
            return True
        if i_prev + 1 < n and j_prev  >= 0 and dist[i_prev * m + j_prev - 0][0] ==  dist[(i_prev + 1) * m + j_prev][0] + matrix[i_prev][j_prev]:
            return True
        if i_prev - 1 >= 0 and j_prev - 1 >= 0 and dist[i_prev * m + j_prev - 1][0] ==  dist[(i_prev - 1) * m + j_prev - 1][0] + matrix[i_prev][j_prev - 1]:
            return True
        if i_prev + 1 < n and j_prev - 1 >= 0 and dist[i_prev * m + j_prev - 1][0] ==  dist[(i_prev + 1) * m + j_prev - 1][0] + matrix[i_prev][j_prev - 1]:
            return True
        if i_prev - 1 >= 0 and j_prev - 2 >= 0 and dist[i_prev * m + j_prev - 2][0] ==  dist[(i_prev - 1) * m + j_prev - 2][0] + matrix[i_prev][j_prev - 2]:
            return True
        if i_prev + 1 < n and j_prev - 2 >= 0 and dist[i_prev * m + j_prev - 2][0] ==  dist[(i_prev + 1) * m + j_prev - 2][0] + matrix[i_prev][j_prev - 2]:
            return True
        if j_prev - 2 < 0:
            return True
    
    if dir == (0, -1):
        prev = (i - i_dir, j - j_dir)
        (i_prev, j_prev) = prev
        if i_prev - 1 >= 0 and j_prev  < m and dist[i_prev * m + j_prev + 0][0] ==  dist[(i_prev - 1) * m + j_prev + 0][0] + matrix[i_prev][j_prev + 0]:
            return True
        if i_prev + 1 < n and j_prev < m and dist[i_prev * m + j_prev + 0][0] ==  dist[(i_prev + 1) * m + j_prev + 0][0] + matrix[i_prev][j_prev + 0]:
            return True
        if i_prev - 1 >= 0 and j_prev + 1 < m and dist[i_prev * m + j_prev + 1][0] ==  dist[(i_prev - 1) * m + j_prev + 1][0] + matrix[i_prev][j_prev + 1]:
            return True
        if i_prev + 1 < n and j_prev + 1 < m and dist[i_prev * m + j_prev + 1][0] ==  dist[(i_prev + 1) * m + j_prev + 1][0] + matrix[i_prev][j_prev + 1]:
            return True
        if i_prev - 1 >= 0 and j_prev + 2 < m and dist[i_prev * m + j_prev + 2][0] ==  dist[(i_prev - 1) * m + j_prev + 2][0] + matrix[i_prev][j_prev + 2]:
            return True
        if i_prev + 1 < n and j_prev + 2 < m and dist[i_prev * m + j_prev + 2][0] ==  dist[(i_prev + 1) * m + j_prev + 2][0] + matrix[i_prev][j_prev + 2]:
            return True
        if j_prev +2 >= m:
            return True
    if dir == (-1, 0):
        prev = (i - i_dir, j - j_dir)
        (i_prev, j_prev) = prev
        if j_prev - 1 >= 0 and i_prev + 0 < n and dist[(i_prev + 0) * m + j_prev][0] ==  dist[(i_prev + 0) * m + j_prev -1][0] + matrix[i_prev + 0][j_prev]:
            return True
        if j_prev + 1 < m and i_prev + 0 < n and dist[(i_prev + 0) * m + j_prev][0] ==  dist[(i_prev + 0) * m + j_prev +1][0] + matrix[i_prev + 0][j_prev]:
            return True
        if j_prev - 1 >= 0 and i_prev + 1 < n and dist[(i_prev + 1) * m + j_prev][0] ==  dist[(i_prev + 1) * m + j_prev -1][0] + matrix[i_prev + 1][j_prev]:
            return True
        if j_prev + 1 < m and i_prev + 1 < n and dist[(i_prev + 1) * m + j_prev][0] ==  dist[(i_prev + 1) * m + j_prev +1][0] + matrix[i_prev + 1][j_prev]:
            return True
        if j_prev - 1 >= 0 and i_prev + 2 < n and dist[(i_prev + 2) * m + j_prev][0] ==  dist[(i_prev + 2) * m + j_prev -1][0] + matrix[i_prev + 2][j_prev]:
            return True
        if j_prev + 1 < m and i_prev + 2 < n and dist[(i_prev + 2) * m + j_prev][0] ==  dist[(i_prev + 2) * m + j_prev +1][0] + matrix[i_prev + 2][j_prev]:
            return True
        if i_prev + 2 >= n:
            return True
    if dir == (1, 0):
        prev = (i - i_dir, j - j_dir)
        (i_prev, j_prev) = prev
        if j_prev - 1 >= 0 and i_prev - 0 >= 0 and dist[(i_prev - 0) * m + j_prev][0] ==  dist[(i_prev - 0) * m + j_prev -1][0] + matrix[i_prev - 0][j_prev]:
            return True
        if j_prev + 1 < m and i_prev - 0 >= 0 and dist[(i_prev - 0) * m + j_prev][0] ==  dist[(i_prev -0) * m + j_prev +1][0] + matrix[i_prev - 0][j_prev]:
            return True
        if j_prev - 1 >= 0 and i_prev - 1 >= 0 and dist[(i_prev - 1) * m + j_prev][0] ==  dist[(i_prev - 1) * m + j_prev -1][0] + matrix[i_prev - 1][j_prev]:
            return True
        if j_prev + 1 < m and i_prev - 1 >= 0 and dist[(i_prev - 1) * m + j_prev][0] ==  dist[(i_prev - 1) * m + j_prev +1][0] + matrix[i_prev - 1][j_prev]:
            return True
        if j_prev - 1 >= 0 and i_prev - 2 >= 0 and dist[(i_prev - 2) * m + j_prev][0] ==  dist[(i_prev - 2) * m + j_prev -1][0] + matrix[i_prev - 2][j_prev]:
            return True
        if j_prev + 1 < m and i_prev - 2 >= 0 and dist[(i_prev - 2) * m + j_prev][0] ==  dist[(i_prev - 2) * m + j_prev +1][0] + matrix[i_prev - 2][j_prev]:
            return True
        if i_prev - 2 < 0:
            return True
    return False

def get_neighbors(pos, pdir, n, m, dist, matrix):
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
        #if dir == skip:
            #continue
        (i_dir, j_dir) = dir
        new_pos = (i + i_dir, j + j_dir)
        print(f"newpos = {new_pos} dir = {dir}")
        if i + i_dir >= 0 and i + i_dir < n and j + j_dir >= 0 and j + j_dir < m and valid_v(new_pos, dir, dist, n, m):
            neighbors.add((new_pos, dir))
    
    return neighbors
    
def minDistance(dist, sptSet, n, m):

        # Initialize minimum distance for next node
    min = sys.maxsize
    min_pos = None
        # Search not nearest vertex not in the
        # shortest path tree
    for i in range(n):
        for j in range(m):
            u = i * m + j
            if dist[u][0] < min and sptSet[u] == False:
                min = dist[u][0]
                min_index = u
                min_pos = (i, j)
                min_dir = dist[u][1]
    print(min_pos)
    if min_pos == None:
        return 
    return min_pos, min_dir

def dijkstra_modif(matrix, starting_pos = (0, 0), starting_dir = (0, 1)):
    valid_dict = dict()
    for dir in DIR:
        valid_dict[dir] = set([starting_pos])
        
    n = len(matrix)
    m = len(matrix[0])
    
    dist = [[sys.maxsize, None] for _ in range (n * m)]
    dist[0] = [0, (0, 1)]
    sptSet = [False] * n * m

    pdir = starting_dir
    for i in range(n):
        for j in range(m):
            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # x is always equal to src in first iteration
            
            xx, pdir = minDistance(dist, sptSet, n, m)
            
            if xx == None:
                break
            valid_dict[pdir].add(xx)
            (i_min, j_min) = xx
            x = i_min * m + j_min
            
            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[x] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            neighbors = get_neighbors(xx, pdir, n, m, dist, matrix)
            print(f"{xx} -> {neighbors}")
            for (neigh_i, neigh_j), dir in neighbors:
                y = neigh_i * m + neigh_j
                dist_x_y = matrix[neigh_i][neigh_j]
                if sptSet[y] == False and dist[y][0] > dist[x][0] + dist_x_y:
                    dist[y][0] = dist[x][0] + dist_x_y
                    dist[y][1] = dir
    for i in range(n):
        for j in range(m):
            print(dist[i * m +j][0], end = " ")
        print()
    print(valid_dict)
    return dist[n * m - 1]
            
    
    


if __name__ == '__main__':
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
    #neighbors = get_neighbors((i_min, j_min), pdir, n, m, dist, matrix)
    #print(f"{xx} -> {neighbors}")
    print(f"Result is {dijkstra_modif(matrix)}")
    