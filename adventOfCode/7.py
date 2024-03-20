from sortedcontainers import SortedList

k5 = []
k4 = []
fh = []
k3 = []
p2 = []
p1 = []
hk = []
card_map = {'A': 13, 'K': 12, 'Q' : 11, 'T': 10, '9' : 9, '8' : 8, '7' : 7, '6' : 6, '5' : 5, '4' : 4, '3' : 3, '2' : 2, 'J': 1}


def compare_card(card1, card2):
    for i, c in enumerate(card1):
        if card_map[c] > card_map[card2[i]]:
            return 1
        elif card_map[c] < card_map[card2[i]]:
            return -1
    return 0

def put_in_stronger_type(cardbid, same):
    global k5
    global k4 
    global fh 
    global k3 
    global p2
    global p1 
    global hk
    
    (card, bid) = cardbid
    
    numJ = same['J']
    same.pop('J')
    print(f"same without J : {same} and numJ = {numJ}")
    
    next_round = False
    if numJ == 5:
        k5 = add_to(k5, (card, bid))
    else:
        for k, v in sorted(same.items(), key=lambda item: item[1], reverse=True):
            if next_round:
                if v == 2:
                    fh = add_to(fh, (card, bid))
                    break
                if v == 1:
                    k3 = add_to(k3, (card, bid))
                    break
            if v == 4:
                k5 = add_to(k5, (card, bid))
                break
            if v == 3:
                if numJ == 1:
                    k4 = add_to(k4, (card, bid))
                    break
                else:
                    k5 = add_to(k5, (card, bid))
                    break
            if v == 2:
                if numJ == 3:
                    k5 = add_to(k5, (card, bid))
                    break
                elif numJ == 2:
                    k4 = add_to(k4, (card, bid))
                    break
                else:
                    next_round = True
            if v == 1:
                if numJ == 4:
                    k5 = add_to(k5, (card, bid))
                    break
                elif numJ == 3:
                    k4 = add_to(k4, (card, bid))
                    break
                elif numJ == 2:
                    k3 = add_to(k3, (card, bid))
                    break
                else:
                    p1 = add_to(p1, (card, bid))
                    break

def rank(cards):
    
    global k5
    global k4 
    global fh 
    global k3 
    global p2
    global p1 
    global hk
    
    for (card, bid) in cards:
        same = dict()
        for c in card:
            if c not in same:
                same[c] = 1
            else:
                same[c] += 1
        print(sorted(same.items(), key=lambda item: item[1], reverse=True))
        print(same)
        if 'J' in card:
            
            print(card)
            put_in_stronger_type((card, bid), same)
        else:
            next_round = False
            nr_elemnet = None
            for k, v in sorted(same.items(), key=lambda item: item[1], reverse=True):
                print(f"k={k}, v={v}")
                if next_round and nr_elemnet == 3:
                    if v == 2:
                        fh = add_to(fh, (card, bid))
                        break
                    else:
                        k3 = add_to(k3, (card, bid))
                        break
                if next_round and nr_elemnet == 2:
                    if v == 2:
                        p2 = add_to(p2, (card, bid))
                        break
                    else:
                        p1 = add_to(p1, (card, bid))
                        break
                if v == 5:
                    k5 = add_to(k5, (card, bid))
                    break
                elif v == 4:
                    k4 = add_to(k4, (card, bid))
                    break
                elif v == 3:
                    next_round = True
                    nr_elemnet = 3
                elif v == 2:
                    next_round = True
                    nr_elemnet = 2
                else:
                    hk = add_to(hk, (card, bid))
                    break
    
    return k5 + k4 + fh + k3 + p2 + p1 + hk

def binarySearch(arr, low, high, cardbid):
    (card, bid) = cardbid
    while low <= high:
        mid = low + (high - low) // 2;
        (card2, _) = arr[mid]
        if compare_card(card, card2) == 0:
            return mid
        elif compare_card(card, card2) == 1:
            high = mid - 1
        else:
            low = mid + 1
    return high

def add_to(list, cardbid):
    if len(list) == 0:
        list.append(cardbid)
        return list
    
    indexpos = binarySearch(list, 0, len(list)-1, cardbid)
    list = list[:indexpos+1] + [cardbid] + list[indexpos+1:]
    return list
            

def f(cards):
    sum = 0
    n = len(cards)
    rank_cards = rank(cards)
    print(n)
    for i, (card, bid) in enumerate(rank_cards):
        print(f"c={card} b={bid} rank={n - i}")
        sum += (n - i) * bid
    print(len(rank_cards))
    return sum
    


if __name__ == '__main__':
    cards = []
    bids = []
    with open('w.txt', 'r') as file:
        for line in file:
            print(line)
            parts = line.split()
            card = parts[0]
            bid = int(parts[1])
            print(f"card={card} bid={bid}")
            cards.append((card, bid))
            
    
    print(f"Total sum is: {f(cards)}")