import re
const = 2
import sys

sys.setrecursionlimit(2**30)
def ff(input):
    result = 0
    i = 0
    for (word, numbers) in input:
        print(i)
        br = find_all_positions(word, numbers)
        #br2 = f(word, numbers)
        #if br != br2:
            #print(i)
            #print(f"'{word}', {numbers}")
            #print(f"brRec = {br} brBruteForce = {br2}")
        #print(f"{i} COMB: {br}")
        result += br
        i+=1
    return result

    
def blocks(word):
    n = len(word)
    b = []
    new_block = []
    new_blocks = []
    for i in range(n + 1):
        if i == n or word[i] == '.':
            new_blocks.append(new_block)
            new_block = []
        else:
            new_block.append(word[i])
    
    for bl in new_blocks:
        if len(bl)!=0:
            b.append(len(bl))
    return b

def checkb(word, numbers):
    #print(blocks(word))
    #print(numbers)
    return blocks(word) == numbers



def f(word, numbers):
    br = 0
    words = get_new_word(word)   
    #print(words)
    for wo in words:
        if checkb(wo, numbers):
            br += 1
    #print(br)
    return br

def get_new_word(word):
    new_words = set()
    brr = 0
    for w in word:
        if w == '?':
            brr+=1
    que = set(["" for _ in range(2**(brr))])
    for w in word:
        new_que = set()
        if w == '?':
            for q in que:
                new_que.add(q + '.')
                new_que.add(q + '#')
        else:
            for q in que:
                new_que.add(q + w)
        que = new_que
    
    return que



############## OPTIMAL #############
def count(word, numbers):
    counter = []
    counter_after = []
    counter_num = []
    upit = 0
    tarab = 0
    for w in word:
        counter.append([tarab, upit])
        if w == '#':
            tarab += 1
        elif w == '?':
            upit += 1
    
    
    for kk, w in enumerate(word):
        if w == '#':
            counter_after.append([tarab - counter[kk][0] -1, upit - counter[kk][1]])
        elif w == '?':
            counter_after.append([tarab - counter[kk][0], upit - counter[kk][1] - 1])
        else:
            counter_after.append([tarab - counter[kk][0], upit - counter[kk][1]])

    all = 0
    for num in numbers:
        all += num
        
    counter_num.append([0, all - numbers[0]])
    for i in range(1, len(numbers)):
        counter_num.append([counter_num[i-1][0] + numbers[i-1], counter_num[i-1][1] - numbers[i]])
    return counter, counter_after, counter_num

def remove_element_from_sorted_list(sorted_list, element_to_remove):
    low, high = 0, len(sorted_list) - 1

    while low <= high:
        mid = (low + high) // 2
        if sorted_list[mid] == element_to_remove:
            del sorted_list[mid]
            return sorted_list
        elif sorted_list[mid] < element_to_remove:
            low = mid + 1
        else:
            high = mid - 1

    # If the element is not found, you can handle this case based on your requirements.
    #print(f"Element {element_to_remove} not found in the list.")
    return sorted_list

def find_possible_positions(word, numbers):
    all_pos = []
    n = len(word) 
    
    counter, counter_after, counter_num = count(word, numbers)

    
    for kk, num in enumerate(numbers):
        
        pos = []
        
        for i in range(n):
            if i + num > n:
                break
            if (word[i] == '?' or word[i] == '#') and i + num <= n:
                j = 0
                possible_pos = True
                while j < num:
                    if not (word[i + j] == '?' or word[i + j] =='#'):
                        possible_pos = False
                        break
                    j += 1
                if possible_pos and (i == 0 or word[i - 1] != '#') and (i + num == n or word[i + num] != '#'):
                    pos.append(i)
        
        print(f"{num} before ---> {pos}")
        d = 0
        g = len(pos)
        #print(f"d = {d} g = {g}")
        for pi, p in enumerate(pos):
            if counter[p][0] > counter_num[kk][0] or (counter_after[p + num - 1][0] + counter_after[p + num - 1][1]) < counter_num[kk][1] :
                #print(f"prvo {p}")
                
                #pos = pos[:pi]
                g = pi
                #print(f"g = {g}")
            
            elif (counter[p][0] + counter[p][1]) < counter_num[kk][0] or counter_after[p + num - 1][0] > counter_num[kk][1]:
                #print(counter_num)
                #print(f"({counter[p][0]} + {counter[p][1]}) < {counter_num[kk][0]} or {counter_after[p + num - 1][0]} > {counter_num[kk][1]}")
                #print(f"drugo {p} {pi}")
                #pos = pos[pi:]
                d = pi
                #print(f"d = {d}")
            #print(f"d = {d} g = {g}")
        
        print(f"{num} after ---> {pos[d:g]}")    
        
        all_pos.append(pos[d:g])
    return all_pos

def binary_search_first_greater_index(lst, target):
    left, right = 0, len(lst) - 1
    result_index = None

    while left <= right:
        mid = (left + right) // 2

        if lst[mid] > target:
            result_index = mid
            right = mid - 1  # Look for a smaller element on the left
        else:
            left = mid + 1   # Look for a greater element on the right

    return result_index

def find_next_pos(pos, next_pos):
    if pos < next_pos[0]:
        return next_pos
    if pos >= next_pos[len(next_pos) - 1]:
        return []
    ind = binary_search_first_greater_index(next_pos, pos)
    return next_pos[ind:]

def find_all_positions(word, numbers):
    all_pos = find_possible_positions(word, numbers)
    
    #print(all_pos)
    
    n = len(all_pos)
    m = len(numbers)
    
    next_pos_lists = [None for _ in range(n)]
    next_pos_lists[0] = all_pos[0]
    tag_list = set()
    for i, w in enumerate(word):
        if w == '#':
            tag_list.add(i)
    return rec(all_pos[0], 1, n, numbers, all_pos, next_pos_lists, [], tag_list, 0)

def rec(first, i, n, numbers, all_pos, next_pos_lists, deq, tag_list, j):
    #print("-------------")
    #print(first)
    #print(i)
    if i == 1 and len(first) == 0:
        return 0
    if len(first) == 0:
        next_pos_lists[i - 2] = next_pos_lists[i - 2][1:]
        return rec(next_pos_lists[i - 2], i - 1 , n, numbers, all_pos, next_pos_lists, deq, tag_list, j)
    p = first[0]
    deq = deq[:i - 1] + [p]
    next_pos_lists[i] = find_next_pos(p + numbers[i - 1], all_pos[i])
    #print(next_pos_lists[i])
    #print("-------------")
    j+=1
    
    if len(next_pos_lists[i]) == 0:
        if i >= 2:
            next_pos_lists[i - 1] = next_pos_lists[i - 1][1:]
            return rec(next_pos_lists[i - 1], i, n, numbers, all_pos, next_pos_lists, deq, tag_list, j)
        else:
            return 0
        
    if i == n - 1:
        # reach last numbers
        
        next_pos_lists[i - 1] = next_pos_lists[i - 1][1:]
        numm = num_of_possibilities(deq, next_pos_lists[i], tag_list, numbers)
        return numm + rec(next_pos_lists[i - 1], i, n, numbers, all_pos, next_pos_lists, deq, tag_list, j)
    

    #if j == 5:
        #return 
    # find possible pos for next number
    return rec(next_pos_lists[i], i + 1, n, numbers, all_pos, next_pos_lists, deq, tag_list, j)
        
def num_of_possibilities(positions, candidate_for_last_position, hash_positions, numbers):
    #print(f"hash_positions = {hash_positions}")
    result = 0
    index_list = set()
    #print(f"POS: {positions}")
    for i, position in enumerate(positions):
        for j in range(position, position + numbers[i]):
            index_list.add(j)
    #print(index_list)
    for candidate in candidate_for_last_position:
        #print(f"CAND: {candidate}")
        cand_index_list = set()
        for j in range(candidate, candidate + numbers[len(numbers) - 1]):
            cand_index_list.add(j)
        #print(f"candindexlist: {cand_index_list}")
        valid_combination = True
        for hash_position in hash_positions:
            if hash_position not in index_list and hash_position not in cand_index_list:
                valid_combination = False
                break
        
        if valid_combination:
            result += 1
    
    #print(f"result --> {result}")
    return result

if __name__ == '__main__':
    positions = []
    file_name = 'input12.txt'
    
    with open(file_name, 'r') as file:
        inputs = []
        for line in file:
            numbers = []
            parts = line.split(" ")
            word = parts[0]
            for num in parts[1].split(","):
                numbers.append(int(num))
                
            new_word = ""
            new_numbers = []
            for i in range(5):
                new_word += "?" + word 
                new_numbers += numbers
            
            inputs.append((new_word, new_numbers))
            #inputs.append((word, numbers))
    
    #print(inputs)
    
    #bl = find_next_pos(10, [9,10])
    #bl = find_all_positions('????????#????#?#?.??', [1,1,1,1,4,2])
    
    
    #bl = find_all_positions('?#?????#??.???#?.', [2,2,3,3])
    #print(bl)
    #print(f('?#?????#??.???#?.', [2,2,3,3]))
    print(f"Sum is: {ff(inputs)}")
    #print(find_next_pos(3, [3, 5, 9, 10, 11, 12, 14]))