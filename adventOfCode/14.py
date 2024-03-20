
CONST = 1000000000
def f(matrix, all_positions):
    n = len(matrix)
    m = len(matrix[0])
    
    for i in range(1, n):
        remove_positions = set()
        for pos in all_positions[i]:
            if pos not in all_positions[i - 1] and matrix[i - 1][pos] == '.':
                remove_positions.add(pos)
                all_positions[i - 1].add(pos)
        for pos in remove_positions:
            all_positions[i].remove(pos)
    
    result = 0
    for i in range(n):
        print(n-i)
        print(all_positions[i])
        result += (n - i) * len(all_positions[i])
        
    return result

def preprocess(matrix):
    n = len(matrix)
    m = len(matrix[0])
    matrix_num = [[[0,0,0,0] for _ in range(m)] for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            # up
            if i == 0:
                matrix_num[i][j][0] = 0
            else:
                if matrix[i - 1][j] == '#':
                    matrix_num[i][j][0] = 0
                else:
                    matrix_num[i][j][0] = matrix_num[i - 1][j][0] + int(matrix[i - 1][j] == '.')
            
            # left
            if j == 0:
                matrix_num[i][j][2] = 0
            else:
                if matrix[i][j - 1] == '#':
                    matrix_num[i][j][2] = 0
                else:
                    matrix_num[i][j][2] = matrix_num[i][j - 1][2] + int(matrix[i][j - 1] == '.')
                    
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):       
            # down
            if i == n - 1:
                matrix_num[i][j][1] = 0
            else:
                if matrix[i + 1][j] == '#':
                    matrix_num[i][j][1] = 0
                else:
                    matrix_num[i][j][1] = matrix_num[i + 1][j][1] + int(matrix[i + 1][j] == '.')
            
            #right
            if j == m - 1:
                matrix_num[i][j][3] = 0
            else:
                if matrix[i][j + 1] == '#':
                    matrix_num[i][j][3] = 0
                else:
                    matrix_num[i][j][3] = matrix_num[i][j + 1][3] + int(matrix[i][j + 1] == '.')
    
    print(matrix_num)
    return matrix_num
            
def tilt_north_optimal(matrix_num, all_positions=None):
    n = len(matrix)
    m = len(matrix[0])
    
    for i in range(1, n):
        print(all_positions[i])
        to_remove = set()
        for j in all_positions[i]:
            k = matrix_num[i][j][0]
            if k != 0:
                print(j)
                to_remove.add(j)
                print(to_remove)
                all_positions[i - k].add(j)
                
                # update matrix_num for down
                for l in range(i - 1, i - k + 1):
                    matrix_num[l][j][1] += 1
                    
                # update matrix_num for up
                if i != n - 1:
                    for l in range(i + 1, i + matrix_num[i][j][1]):
                        matrix_num[l][j][0] += matrix_num[i][j][0] + 1
            
        for el in to_remove:
            all_positions[i].remove(el)
        
def tilt_south_optimal(matrix_num, all_positions=None):
    n = len(matrix)
    m = len(matrix[0])
    
    for i in range(n - 2, -1, -1):
        print(all_positions[i])
        to_remove = set()
        for j in all_positions[i]:
            k = matrix_num[i][j][1]
            if k != 0:
                to_remove.add(j)
                print(to_remove)
                all_positions[i + k].add(j)
                
                # update matrix_num
                for l in range(i):
                    matrix_num[l][j][0] += matrix_num[i][j][0] + 1
                    
            
        for el in to_remove:
            all_positions[i].remove(el)

def tilt_north(matrix, all_positions=None):
    n = len(matrix)
    m = len(matrix[0])
    
    for i in range(1, n):
        for j in range(m):
            el = matrix[i][j]
            if el == 'O':
                k = i - 1
                while k > -1 and matrix[k][j] == '.':
                    k -= 1
                if k + 1 != i:
                    matrix[k + 1][j] = 'O'
                    matrix[i][j] = '.'
                    all_positions[k + 1].add(j)
                    all_positions[i].remove(j)

def tilt_south(matrix, all_positions=None):
    n = len(matrix)
    m = len(matrix[0])
    
    for i in range(n - 2, -1, -1):
        for j in range(m):
            el = matrix[i][j]
            if el == 'O':
                k = i + 1
                while k < n and matrix[k][j] == '.':
                    k += 1
                if k != i + 1:
                    matrix[k - 1][j] = 'O'
                    matrix[i][j] = '.'
                    all_positions[k - 1].add(j)
                    all_positions[i].remove(j)

def tilt_east(matrix, all_positions=None):
    n = len(matrix)
    m = len(matrix[0])
    
    for j in range(m - 2, -1, -1):
        for i in range(n):
            el = matrix[i][j]
            if el == 'O':
                k = j + 1
                while k < m and matrix[i][k] == '.':
                    k += 1
                if k != j + 1:
                    matrix[i][k - 1] = 'O'
                    matrix[i][j] = '.'
                    all_positions[i].add(k - 1)
                    all_positions[i].remove(j)

def tilt_west(matrix, all_positions=None):
    n = len(matrix)
    m = len(matrix[0])
    
    for j in range(1, m):
        for i in range(n):
            el = matrix[i][j]
            if el == 'O':
                k = j - 1
                while k > -1 and matrix[i][k] == '.':
                    k -= 1
                if k + 1 != j:
                    matrix[i][k + 1] = 'O'
                    matrix[i][j] = '.'
                    all_positions[i].add(k + 1)
                    all_positions[i].remove(j)

def ff(all_positions):
    
    n = len(all_positions)
    result = 0
    for i in range(n):
        print(n-i)
        print(all_positions[i])
        result += (n - i) * len(all_positions[i])
        
    return result



def binary_search_first_smaller(arr, target):
    left, right = 0, len(arr) - 1
    result = -1  # Initialize the result to -1 in case no smaller element is found

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] < target:
            result = mid  # Update result and continue searching on the right side
            left = mid + 1
        else:
            right = mid - 1

def fff(matrix):
    n = len(matrix)
    m = len(matrix[0])
    res = 0
    for i in range(n):
        numO = 0
        for j in range(m):
            if matrix[i][j] == 'O':
                numO+=1
        
        res += (n - i) * numO
    return res
if __name__ == '__main__':
    
    all_positions = []
    matrix = []
    file_name = 'input141.txt'
    result = 0
    
    with open(file_name, 'r') as file:
        for line in file:
            row = line.strip()
            matrix_row = []
            positions = set()
            for i, element in enumerate(row):
                matrix_row.append(element)
                if element == 'O':
                    positions.add(i)
            all_positions.append(positions)
            matrix.append(matrix_row)
            
    #print(all_positions)
    k = 100
    for i in range(0):
        if i%1000000 == 0:
            print(i)
        tilt_north(matrix, all_positions)
        tilt_west(matrix, all_positions)
        tilt_south(matrix, all_positions)
        tilt_east(matrix, all_positions)
    matrix_num = preprocess(matrix)
    tilt_north_optimal(matrix_num, all_positions)
    print(f"Result is: {ff(all_positions)}")
    