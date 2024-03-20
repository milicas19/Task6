
import copy
from collections import deque

def go_pos(char, start_pos, n, m):
    """ (up, down, left, right)"""
    if char == "|":
        pos =  [1, 1, 0, 0]
    elif char == "-":
        pos = [0, 0, 1, 1]
    elif char == "L":
        pos = [1, 0, 0, 1]
    elif char == "J":
        pos = [1, 0, 1, 0]
    elif char == "7":
        pos = [0, 1, 1, 0]
    elif char == "F":
        pos = [0, 1, 0 , 1]
    elif char == ".":
        pos = [0, 0, 0 , 0]
    elif char == "S":
        pos = [1, 1, 1, 1]
    
    (i, j) = start_pos
    if i == 0:
        pos[0] = 0
    elif i == n - 1:
        pos[1] = 0
            
    if j == 0:
        pos[2] = 0
    elif j == m - 1:
        pos[3] = 0
    
    return pos

def find_inner(instr_matrix_copy, starting_pos, pos_matrix):
    all = 0
    for l in pos_matrix:
        for e in l:
            if e == -1:
                all += 1

    r_loop, l_loop = path(instr_matrix_copy, starting_pos, pos_matrix)
    
    if len(r_loop) < len(l_loop):
        loop = r_loop
    else:
        loop = l_loop
        
    n = len(pos_matrix)
    m = len(pos_matrix[0])
    
    red = deque(loop)
    # print(len(loop))
    br = 0
    while red:
        elem = red.popleft()
        (i, j) = elem
        br += 1
        
        if i != 0 and j != 0 and pos_matrix[i - 1][j - 1] == -1 and (i - 1, j - 1) not in loop:
                red.append((i - 1, j - 1))
                loop.add((i - 1, j - 1))
                
        if i != 0 and pos_matrix[i - 1][j] == -1 and (i - 1, j) not in loop:
                red.append((i - 1, j))
                loop.add((i - 1, j))
        
        if i != 0 and j != m - 1 and pos_matrix[i - 1][j + 1] == -1 and (i - 1, j + 1) not in loop:
                red.append((i - 1, j + 1))
                loop.add((i - 1, j + 1))
                
        if j != 0 and pos_matrix[i][j - 1] == -1 and (i, j - 1) not in loop:
                red.append((i, j - 1))
                loop.add((i, j - 1))
        
        if j != m - 1 and pos_matrix[i][j + 1] == -1 and (i, j + 1) not in loop:
                red.append((i, j + 1))
                loop.add((i, j + 1))
        
        if i != n - 1 and j != 0 and pos_matrix[i + 1][j - 1] == -1 and (i + 1, j - 1) not in loop:
                red.append((i + 1, j - 1))
                loop.add((i + 1, j - 1))    
        
        if i != n - 1 and pos_matrix[i + 1][j] == -1 and (i + 1, j) not in loop:
                red.append((i + 1, j))
                loop.add((i + 1, j)) 
        
        if i != n - 1 and j != m - 1 and pos_matrix[i + 1][j + 1] == -1 and (i + 1, j + 1) not in loop:
                red.append((i + 1, j + 1))
                loop.add((i + 1, j + 1))

    correct_tiles = check(loop, n, m, pos_matrix)
    # print(correct_tiles)
    
    if correct_tiles:
        return br
    else:
        return all - br
                        
def check(loop, n, m, pos_matrix):
    for j in range(m):
        if (0, j) in loop and pos_matrix[0][j] == -1:
            return 0
        if (n - 1, j) in loop and pos_matrix[n - 1][j] == -1:
            return 0
    for i in range(n):
        if (i, 0) in loop and pos_matrix[i][0] == -1:
            return 0
        if (i, m - 1) in loop and pos_matrix[i][m - 1] == -1:
            return 0
    
    return 1

def path(instr_matrix_copy, starting_pos, pos_matrix):
    n = len(instr_matrix_copy)
    m = len(instr_matrix_copy[0])
    
    left_from_loop = set()
    right_from_loop = set()
        
    full_circle = False
    lenpath = 0
    start = starting_pos
    while not full_circle:
        lenpath += 1
        (start_i, start_j) = start
        # print(f"s={start}")
        next = None
        start_go_pos = instr_matrix_copy[start_i][start_j]
        # UP
        if start_go_pos[0] == 1:
            poss_next_go_pos = instr_matrix_copy[start_i - 1][start_j]
            if poss_next_go_pos[1] == 1:
                next = (start_i - 1, start_j)
                instr_matrix_copy[start_i - 1][start_j][1] = 0
                
                if start_j != 0 and pos_matrix[start_i][start_j - 1] ==  -1:
                    left_from_loop.add((start_i, start_j - 1))
                if start_j != m - 1 and  pos_matrix[start_i][start_j + 1] ==  -1:
                    right_from_loop.add((start_i, start_j + 1))
                    
                if start_i != 0 and start_j != 0 and pos_matrix[start_i - 1][start_j - 1] ==  -1:
                    left_from_loop.add((start_i - 1, start_j - 1))
                if start_i != 0 and start_j != m - 1 and  pos_matrix[start_i - 1][start_j + 1] ==  -1:
                    right_from_loop.add((start_i - 1, start_j + 1))
        # DOWN
        if next == None and start_go_pos[1] == 1:
            poss_next_go_pos = instr_matrix_copy[start_i + 1][start_j]
            if poss_next_go_pos[0] == 1:
                next = (start_i + 1, start_j)
                instr_matrix_copy[start_i + 1][start_j][0] = 0
                
                if start_j != 0 and pos_matrix[start_i][start_j - 1] ==  -1:
                    right_from_loop.add((start_i, start_j - 1))
                if start_j != m - 1 and  pos_matrix[start_i][start_j + 1] ==  -1:
                    left_from_loop.add((start_i, start_j + 1))
                
                if start_i != n - 1 and start_j != 0 and pos_matrix[start_i + 1][start_j - 1] ==  -1:
                    right_from_loop.add((start_i + 1, start_j - 1))
                if start_i != n - 1 and start_j != m - 1 and pos_matrix[start_i + 1][start_j + 1] ==  -1:
                    left_from_loop.add((start_i + 1, start_j + 1))
        # LEFT
        if next == None and start_go_pos[2] == 1:
            poss_next_go_pos = instr_matrix_copy[start_i][start_j - 1]
            if poss_next_go_pos[3] == 1:
                next = (start_i, start_j - 1)
                instr_matrix_copy[start_i][start_j - 1][3] = 0
                
                if start_i != 0 and pos_matrix[start_i - 1][start_j] ==  -1:
                    right_from_loop.add((start_i - 1, start_j))
                if start_i != n - 1 and pos_matrix[start_i + 1][start_j] ==  -1:
                    left_from_loop.add((start_i + 1, start_j))
                
                if start_i != 0 and start_j != 0 and pos_matrix[start_i - 1][start_j - 1] ==  -1:
                    right_from_loop.add((start_i - 1, start_j - 1))
                if start_i != n - 1 and start_j != 0 and pos_matrix[start_i + 1][start_j - 1] ==  -1:
                    left_from_loop.add((start_i + 1, start_j - 1))
        # RIGHT    
        if next == None and start_go_pos[3] == 1:
            poss_next_go_pos = instr_matrix_copy[start_i][start_j + 1]
            if poss_next_go_pos[2] == 1:
                next = (start_i, start_j + 1)
                instr_matrix_copy[start_i][start_j + 1][2] = 0
                
                if start_i != 0 and pos_matrix[start_i - 1][start_j] ==  -1:
                    left_from_loop.add((start_i - 1, start_j))
                if start_i != n - 1 and pos_matrix[start_i + 1][start_j] ==  -1:
                    right_from_loop.add((start_i + 1, start_j))
                
                if start_i != 0 and start_j != m - 1 and pos_matrix[start_i - 1][start_j + 1] ==  -1:
                    left_from_loop.add((start_i - 1, start_j + 1))
                if start_i != n - 1 and start_j != m - 1 and pos_matrix[start_i + 1][start_j + 1] ==  -1:
                    right_from_loop.add((start_i + 1, start_j + 1))
        
        
        start = next
        if start == starting_pos:
            full_circle = True
            print(f"lenpath = {lenpath}")
        
    return right_from_loop, left_from_loop

def find_furthest(instr_matrix, starting_pos):
    (start_i, start_j) = starting_pos
    n = len(instr_matrix)
    m = len(instr_matrix[0])
    pos_matrix = [[-1 for _ in range(m)] for _ in range(n)]
    pos_matrix[start_i][start_j] = 0
    #print(pos_matrix)
    
    starts = [starting_pos]
    br = 0
    while len(starts):
        #print(starts)
        
        br += 1
        nexts = []
        for start in starts:
            (start_i, start_j) = start
            start_go_pos = instr_matrix[start_i][start_j]
            if start_go_pos[0] == 1:
                poss_next_go_pos = instr_matrix[start_i - 1][start_j]
                if poss_next_go_pos[1] == 1:
                    nexts.append((start_i - 1, start_j))
                    instr_matrix[start_i - 1][start_j][1] = 0
                    if pos_matrix[start_i - 1][start_j] == -1 or pos_matrix[start_i - 1][start_j] > br:
                        pos_matrix[start_i - 1][start_j] = br 
            if start_go_pos[1] == 1:
                poss_next_go_pos = instr_matrix[start_i + 1][start_j]
                if poss_next_go_pos[0] == 1:
                    nexts.append((start_i + 1, start_j))
                    instr_matrix[start_i + 1][start_j][0] = 0
                    if pos_matrix[start_i + 1][start_j] == -1 or pos_matrix[start_i + 1][start_j] > br:
                        pos_matrix[start_i + 1][start_j] = br
            if start_go_pos[2] == 1:
                poss_next_go_pos = instr_matrix[start_i][start_j - 1]
                if poss_next_go_pos[3] == 1:
                    nexts.append((start_i, start_j - 1))
                    instr_matrix[start_i][start_j - 1][3] = 0
                    if pos_matrix[start_i][start_j - 1] == -1 or pos_matrix[start_i][start_j - 1] > br:
                        pos_matrix[start_i][start_j - 1] = br 
            if start_go_pos[3] == 1:
                poss_next_go_pos = instr_matrix[start_i][start_j + 1]
                if poss_next_go_pos[2] == 1:
                    nexts.append((start_i, start_j + 1))
                    instr_matrix[start_i][start_j + 1][2] = 0
                    if pos_matrix[start_i][start_j + 1] == -1 or pos_matrix[start_i][start_j + 1] > br:
                        pos_matrix[start_i][start_j + 1] = br 
        starts = nexts

    furthest = 0
    for el_list in pos_matrix:
        for el in el_list:
            if el > furthest:
                furthest = el

    return pos_matrix

if __name__ == '__main__':
    instr_matrix = []
    instr_matrix_copy = []
    starting_pos = None
    file_name = 'input10.txt'
    with open(file_name, 'r') as file:
        n = sum(1 for line in file)
        
    with open(file_name, 'r') as file:
        i = 0
        for line in file:
            m = len(line.strip())
            instructions = []
            for j, instr in enumerate(line.strip()):
                if instr == "S":
                    starting_pos = (i, j)
                go = go_pos(instr, (i, j), n, m) 
                instructions.append(go)
            instr_matrix.append(instructions)
            instr_matrix_copy.append(copy.deepcopy(instructions))
            i += 1
    
    pos_matrix = find_furthest(instr_matrix, starting_pos)
    print(f"Number of tiles enclosed by the loop is: {find_inner(instr_matrix_copy, starting_pos, pos_matrix)}")
