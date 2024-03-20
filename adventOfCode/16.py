from collections import deque

def correct_pos(pos, n, m):
    (i, j) = pos
    if i >= 0 and i < n and j >= 0 and j < m:
        return 1
    return 0

def add_next_pos(pos, next_dir, dir_map, next_poss, n, m):
    (i, j) = pos
    if (i, j) not in dir_map:
            dir_map[(i, j)] = set()
            dir_map[(i, j)].add(next_dir)
            next_pos = (i + next_dir[0], j + next_dir[1])
            if correct_pos(next_pos, n, m):
                next_poss.append((next_pos, next_dir))
    else:
        if next_dir not in dir_map[(i, j)]:
            dir_map[(i, j)].add(next_dir)
            next_pos = (i + next_dir[0], j + next_dir[1])
            if correct_pos(next_pos, n, m):
                next_poss.append((next_pos, next_dir))
    
    return next_poss

def next_positions(matrix, pos_dir, dir_map, next_poss):
    (i, j), dir = pos_dir
    curr = matrix[i][j]
    n = len(matrix)
    m = len(matrix[0])
    #print(curr)
    
    if curr == '.':
        add_next_pos((i, j), dir, dir_map, next_poss, n, m)
    elif curr == '/':
        if dir == (0, 1):
            next_dir = (-1, 0)
        elif dir == (1, 0):
            next_dir = (0, -1)
        elif dir == (-1, 0):
            next_dir = (0, 1)
        elif dir == (0, -1):
            next_dir = (1, 0)   

        add_next_pos((i, j), next_dir, dir_map, next_poss, n, m)
    elif curr == '\\':
        if dir == (0, 1):
            next_dir = (1, 0)
        elif dir == (1, 0):
            next_dir = (0, 1)
        elif dir == (-1, 0):
            next_dir = (0, -1)
        elif dir == (0, -1):
            next_dir = (-1, 0)    
        
        add_next_pos((i, j), next_dir, dir_map, next_poss, n, m)
    elif curr == '|':
        if dir == (0, 1) or dir == (0, -1):
            next_dir_1 = (-1, 0)
            next_dir_2 = (1, 0)
            add_next_pos((i, j), next_dir_1, dir_map, next_poss, n, m)
            add_next_pos((i, j), next_dir_2, dir_map, next_poss, n, m)
        else:
            add_next_pos((i, j), dir, dir_map, next_poss, n, m)
    elif curr == '-':
        if dir == (0, 1) or dir == (0, -1):
            add_next_pos((i, j), dir, dir_map, next_poss, n, m)
        else:
            next_dir_1 = (0, 1)
            next_dir_2 = (0, -1)
            add_next_pos((i, j), next_dir_1, dir_map, next_poss, n, m)
            add_next_pos((i, j), next_dir_2, dir_map, next_poss, n, m)
            
    return next_poss

def f(matrix, first_pos):
    dir_map = dict()
    next_poss = deque()
    next_poss.append(first_pos)
    visited = set()
    
    while next_poss:
        #print(next_poss)
        pos_dir = next_poss.popleft()
        pos, _ = pos_dir
        visited.add(pos)
        next_poss = next_positions(matrix, pos_dir, dir_map, next_poss)

    return len(visited)

def ff(matrix):
    n = len(matrix)
    m = len(matrix[0])
    max = 0
    for j in range(m):
        down = f(matrix, ((0, j), (1, 0)))
        if down > max:
            max = down
        up = f(matrix, ((n - 1, j), (-1, 0)))
        if up > max:
            max = up
            
    for i in range(n):
        right = f(matrix, ((i, 0), (0, 1)))
        if right > max:
            max = right
        left = f(matrix, ((i, m - 1), (0, -1)))
        if left > max:
            max = left
            
    return max
    

if __name__ == '__main__':
    matrix = []
    file_name = 'inpput16.txt'
    
    with open(file_name, 'r') as file:
        inputs = []
        for line in file:
            row = line.strip()
            matrix.append(row)
    
    print(f"Result is {ff(matrix)}")