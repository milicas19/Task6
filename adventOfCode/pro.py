from sortedcontainers import SortedList


card_map = {'A': 14, 'K': 13, 'Q' : 12, 'J' : 11, 'T': 10, '9' : 9, '8' : 8, '7' : 7, '6' : 6, '5' : 5, '4' : 4, '3' : 3, '2' : 2}


def compare_card(card1, card2):
    for i, (c,b) in enumerate(card1):
        if card_map[c] > card_map[card2[i]]:
            return 1
        elif card_map[c] < card_map[card2[i]]:
            return -1
    return 0

if __name__ == '__main__':
    k5 = SortedList(key=compare_card)    
    k5.add(('99999', 7))
    k5.add(('AAAAA', 5))
    k5.add(('QQQQQ', 19))