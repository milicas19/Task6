CONST = 1000000000
import copy
def preprocess(matrix):
    n = len(matrix)
    m = len(matrix[0])
    all_pos_i = [set() for i in range(n)]
    all_pos_j = [set() for i in range(m)]
    all_tar_pos_i = [[] for i in range(n)]
    all_tar_pos_j = [[] for i in range(m)]
    
    
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 'O':
                all_pos_i[i].add(j)
            elif matrix[i][j] == '#':
                all_tar_pos_i[i].append(j)
    
    for j in range(m):
        for i in range(n):
            if matrix[i][j] == 'O':
                all_pos_j[j].add(i)
            elif matrix[i][j] == '#':
                all_tar_pos_j[j].append(i)
                
    return all_pos_i, all_tar_pos_i, all_pos_j, all_tar_pos_j


def tilt_north(all_pos_j, all_tar_pos_j, n, m, all_pos_i):
    for j in range(m):
        prev = -1
        for tar_pos in all_tar_pos_j[j]:
            
            if tar_pos == prev + 1:
                prev += 1
                continue
            
            to_remove = set()
            for el in all_pos_j[j]:
                if el < tar_pos and el > prev:
                    to_remove.add(el)
                
            
            # update pos j and i 
            for el_rm in to_remove:
                all_pos_j[j].remove(el_rm)
                all_pos_i[el_rm].remove(j)
            for k in range(len(to_remove)):
                all_pos_j[j].add(k + prev + 1)
                all_pos_i[k + prev + 1].add(j)
            
            prev = tar_pos
            
        if prev != n - 1:
            to_remove = set()
            for el in all_pos_j[j]:
                if el < n and el > prev:
                    to_remove.add(el)
            
            # update pos j and i 
            for el_rm in to_remove:
                all_pos_j[j].remove(el_rm)
                all_pos_i[el_rm].remove(j)
            for k in range(len(to_remove)):
                all_pos_j[j].add(k + prev + 1)
                all_pos_i[k + prev + 1].add(j)
    return all_pos_i, all_pos_j 


def tilt_south(all_pos_j, all_tar_pos_j, n, m, all_pos_i):
    for j in range(m):
        prev = -1
        
        for tar_pos in all_tar_pos_j[j]:
            
            if tar_pos == prev + 1:
                prev += 1
                continue
            
            to_remove = set()
            for el in all_pos_j[j]:
                if el < tar_pos and el > prev:
                    to_remove.add(el)
                
            
            # update pos j and i 
            for el_rm in to_remove:
                all_pos_j[j].remove(el_rm)
                all_pos_i[el_rm].remove(j)
            for k in range(len(to_remove)):
                all_pos_j[j].add(tar_pos - 1 - k)
                all_pos_i[tar_pos - 1 - k].add(j)
            
            prev = tar_pos
            
        if prev != n - 1:
            to_remove = set()
            for el in all_pos_j[j]:
                if el < n and el > prev:
                    to_remove.add(el)
            
            # update pos j and i 
            for el_rm in to_remove:
                all_pos_j[j].remove(el_rm)
                all_pos_i[el_rm].remove(j)
            for k in range(len(to_remove)):
                all_pos_j[j].add(n - 1 - k)
                all_pos_i[n - 1 - k].add(j)
                
    return all_pos_i, all_pos_j 


def tilt_west(all_pos_j, all_tar_pos_i, n, m, all_pos_i):
    for i in range(n):
        prev = -1
        for tar_pos in all_tar_pos_i[i]:
            
            if tar_pos == prev + 1:
                prev += 1
                continue
            
            to_remove = set()
            for el in all_pos_i[i]:
                if el < tar_pos and el > prev:
                    to_remove.add(el)
                
            
            # update pos j and i 
            for el_rm in to_remove:
                all_pos_i[i].remove(el_rm)
                all_pos_j[el_rm].remove(i)
            for k in range(len(to_remove)):
                all_pos_i[i].add(prev + 1 + k)
                all_pos_j[prev + 1 + k].add(i)
            
            prev = tar_pos
            
        if prev != m - 1:
            to_remove = set()
            for el in all_pos_i[i]:
                if el < m and el > prev:
                    to_remove.add(el)
            
            # update pos j and i 
            for el_rm in to_remove:
                all_pos_i[i].remove(el_rm)
                all_pos_j[el_rm].remove(i)
            for k in range(len(to_remove)):
                all_pos_i[i].add(prev + 1 + k)
                all_pos_j[prev + 1 + k].add(i)
                
    return all_pos_i, all_pos_j 

def tilt_east(all_pos_j, all_tar_pos_i, n, m, all_pos_i):
    for i in range(n):
        prev = -1
        for tar_pos in all_tar_pos_i[i]:
            
            if tar_pos == prev + 1:
                prev += 1
                continue
            
            to_remove = set()
            for el in all_pos_i[i]:
                if el < tar_pos and el > prev:
                    to_remove.add(el)
                
            
            # update pos j and i 
            for el_rm in to_remove:
                all_pos_i[i].remove(el_rm)
                all_pos_j[el_rm].remove(i)
            for k in range(len(to_remove)):
                all_pos_i[i].add(tar_pos - 1 - k)
                all_pos_j[tar_pos - 1 - k].add(i)
            
            prev = tar_pos
            
        if prev != m - 1:
            to_remove = set()
            for el in all_pos_i[i]:
                if el < m and el > prev:
                    to_remove.add(el)
            
            # update pos j and i 
            for el_rm in to_remove:
                all_pos_i[i].remove(el_rm)
                all_pos_j[el_rm].remove(i)
            for k in range(len(to_remove)):
                all_pos_i[i].add(m - 1 - k)
                all_pos_j[m - 1 - k].add(i)
                
    return all_pos_i,  all_pos_j 

def f(all_pos_i):
    n = len(all_pos_i)
    res = 0
    for i in range(n):
        res += (n - i) * len(all_pos_i[i])
    return res

    
if __name__ == '__main__':
    matrix = []
    file_name = 'input14.txt'
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
            matrix.append(matrix_row)

    n = len(matrix)
    m = len(matrix[0])
            
    all_pos_i, all_tar_pos_i, all_pos_j, all_tar_pos_j = preprocess(matrix)
    with open('out141.txt', 'r') as file:
        for i in range(8410):
            print(i)
            if i!=0 and i % 20000 == 0:
                file.write(f"{all_pos_i}")
                file.write("\n")
                print(all_pos_i)
                #print(all_pos_j)
            #prev = copy.deepcopy(all_pos_i)
            tilt_north(all_pos_j, all_tar_pos_j, n, m, all_pos_i)
            tilt_west(all_pos_j, all_tar_pos_i, n, m, all_pos_i)
            tilt_south(all_pos_j, all_tar_pos_j, n, m, all_pos_i)
            tilt_east(all_pos_j, all_tar_pos_i, n, m, all_pos_i)
            #file.write(f"{all_pos_i}")
            #file.write("\n")
            
            #if all(set1 == set2 for set1, set2 in zip(prev, all_pos_i)):
                #break

    #all_pos_i = tilt_north(all_pos_j, all_tar_pos_j, n, m, all_pos_i)

    print(f(all_pos_i))