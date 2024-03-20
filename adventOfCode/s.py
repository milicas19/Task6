def find_all_positions(word, numbers):
    all_pos = []
    for num in numbers:
        all_pos.append(find_possible_positions(word, num))
    
    print(all_pos)
    
    n = len(all_pos)
    m = len(numbers)
    
    next_pos_lists = [None for _ in range(n)]
    next_pos_lists[0] = all_pos[0]
    tag_list = set()
    for i, w in enumerate(word):
        if w == '#':
            tag_list.add(i)
    return rec(all_pos[0], 1, n, numbers, all_pos, next_pos_lists, [], tag_list)

def rec(first, i, n, numbers, all_pos, next_pos_lists, deq, tag_list):
    print("-------------")
    print(first)
    print(i)
    if i == 1 and len(first) == 0:
        return 0
    if len(first) == 0:
        next_pos_lists[i - 2] = next_pos_lists[i - 2][1:]
        return rec(next_pos_lists[i - 2], i - 1 , n, numbers, all_pos, next_pos_lists, deq, tag_list)
    p = first[0]
    deq = deq[:i - 1] + [p]
    next_pos_lists[i] = find_next_pos(p + numbers[i - 1], all_pos[i])
    print(next_pos_lists[i])
    print("-------------")
    
    
    if i == n - 1:
        if len(next_pos_lists[i]) == 0:
            return 0
        # reach last numbers
        next_pos_lists[i - 1] = next_pos_lists[i - 1][1:]
        print(next_pos_lists[i])
        numm = check(deq, next_pos_lists[i], tag_list, numbers)
        return numm + rec(next_pos_lists[i - 1], i, n, numbers, all_pos, next_pos_lists, deq, tag_list)
    
    if len(next_pos_lists[i]) == 0:
        next_pos_lists[i - 1] = next_pos_lists[i - 1][1:]
        return rec(next_pos_lists[i - 1], i, n, numbers, all_pos, next_pos_lists, deq, tag_list)
    
    # find possible pos for next number
    return rec(next_pos_lists[i], i + 1, n, numbers, all_pos, next_pos_lists, deq, tag_list)




def check(deq, list, tag_list, numbers):
    res = 0
    pos = set()
    i = 0
    for el in deq:
        for j in range(el+numbers[i]):
            pos.add(j)
    for l in list:
        for j in range(l+numbers[len(numbers) - 1]):
            pos.add(j)
        
        putin = True
        for tag in tag_list:
            if tag not in pos:
                putin = False
                break
        
        if putin:
            res += 1