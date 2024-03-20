CONST = 1000000

def distance(pos1, pos2, rows, columns):
    (i1, j1) = pos1
    (i2, j2) = pos2
    
    dist = abs(i1 - i2) + abs(j1 - j2)
    
    for i in rows:
        if (i > i1 and i < i2) or (i > i2 and i < i1):
            dist += CONST - 1
    for j in columns:
        if (j > j1 and j < j2) or (j > j2 and j < j1):
            dist += CONST - 1
    
    return dist

def distances_sum(positions, rows, columns):
    result = 0
    n = len(positions)
    
    for i in range(n - 1):
        for j in range(i + 1, n):
            result += distance(positions[i], positions[j], rows, columns)
        
    return result

if __name__ == '__main__':
    positions = []
    file_name = 'input11.txt'
    
    with open(file_name, 'r') as file:
        i = 0
        for line in file:
            j = 0
            for char in line:
                if char == '#':
                    positions.append((i, j))
                j += 1
            i += 1
            

    rows = set([k for k in range(i)])
    columns = set([k for k in range(j)])
    
    for (i, j) in positions:
        if i in rows:
            rows.remove(i)
        if j in columns:
            columns.remove(j)
    
    print(f"Sum is: {distances_sum(positions, rows, columns)}")
    
