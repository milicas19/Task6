
from collections import deque

DEPTH = 64

def check(pos, depth, n,  m, matrix, queue):
    (i, j) = pos
    if i - 1 >= 0 and matrix[i - 1][j] != '#':
        queue.append(((i - 1, j), depth + 1))
    if j - 1>= 0 and matrix[i][j - 1] != '#':
        queue.append(((i, j - 1), depth + 1))
    if i +1 < n and matrix[i + 1][j] != '#':
        queue.append(((i + 1, j), depth + 1))
    if j + 1 < m and matrix[i][j + 1] != '#':
        queue.append(((i, j + 1), depth + 1))

def f(matrix, starting_pos):
    n = len(matrix)
    m = len(matrix[0])
    num = 0
    
    queue = deque()
    queue.append((starting_pos, 0))
    pos_set = set()
    
    while queue:
        (pos, depth) = queue.popleft()
        
        if depth == DEPTH:
            pos_set.add(pos)
            continue
        
        check(pos, depth, n, m, matrix, queue)
    """
    for pos in pos_set:
        (i, j) = pos
        matrix[i][j] = 'O'
    for i in range(n):
        for j in range(m):
            print(matrix[i][j], end=" ")
        print()
    """

    return len(pos_set)

if __name__ == '__main__':
    matrix = []
    file_name = 'input21.txt'
    
    with open(file_name, 'r') as file:
        i = 0
        for line in file:
            row = []
            j = 0
            for char in line.strip():
                if char == 'S':
                    starting_pos = (i, j)
                row.append(char)
                j += 1
            i += 1
            matrix.append(row)
    
    print(f"Number of positions: {f(matrix, starting_pos)}")