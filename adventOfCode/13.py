MISMATCH_NUM = 0

def horizontal_mirror(matrix):
    n = len(matrix)
    m = len(matrix[0])
    pos = None

    for i in range(1, n):
        mirror_pos = True
        mismatch = 0
        for j in range(i):
            if i + j > n - 1:
                break
            for k in range(m):
                if matrix[i - 1 - j][k] != matrix[i + j][k]:
                    mismatch += 1
                    if mismatch > MISMATCH_NUM:
                        mirror_pos = False
                        break
            if mirror_pos == False:
                break
        if mismatch == MISMATCH_NUM:
            pos = i
            break
    
    print(f"Hor pos is: {pos}")
    return pos * 100

def get_column(matrix, j):
    return [row[j] for row in matrix]

def vertical_mirror(matrix):
    n = len(matrix)
    m = len(matrix[0])
    pos = None
    
    for i in range(1, m):
        mirror_pos = True
        mismatch = 0
        for j in range(i):
            if i + j > m - 1:
                break
            for k in range(n):
                if get_column(matrix, i - 1 - j)[k] != get_column(matrix, i + j)[k]:
                    mismatch += 1
                    if mismatch > MISMATCH_NUM:
                        mirror_pos = False
                        break
            if mirror_pos == False:
                break
        if mismatch == MISMATCH_NUM:
            pos = i
            break
        
    print(f"Ver pos is: {pos}")
    return pos
    
        
def mirror(matrix):
    v = vertical_mirror(matrix)
    if v != None:
        return v
    else:
        return horizontal_mirror(matrix)


if __name__ == '__main__':
    matrix = []
    file_name = 'input131.txt'
    result = 0
    
    with open(file_name, 'r') as file:
        next = False
        row = []
        for line in file:
            if next:
                result += mirror(matrix)
                matrix = []
                next = False
            if line.strip().startswith('.') or line.strip().startswith('#'):
                row = line.strip()
                matrix.append(row)
            else:
                next = True
    result += mirror(matrix)
    
    print(f"Sum is: {result}")
