import re

COLORS = ['red', 'green', 'blue']
LIMITS = [12, 13, 14]

def get_info(line):
    # print(line)
    # pattern = r"Game (\d+)"
    # match = re.search(pattern, line)
    # if match:
        # number = match.group(1)
        # print(number)
    # else:
        # print("ERROR - number must be present")
    
    p = 1
    for i, color in enumerate(COLORS):
        pattern = rf'(\d+) {re.escape(color)}'
        matches = re.findall(pattern, line)
        
        max = 0
        for match in matches:
            if int(match) > max:
                max = int(match)
        
        
        # print(f"{color} -> {max}")
        # if max > LIMITS[i]:
            # return 0
        p *= max

    return p

def sum_possible_games(inputs):
    num = 0
    for input in inputs:
        numInp = get_info(input)
        # print(numInp)
        num += int(numInp)
    return num

if __name__ == '__main__':
    inputs = []
    with open('input2.txt', 'r') as file:
        for line in file:
            line = line.strip()
            inputs.append(line)
    
    # text = "Game 12: 10 red, 2 green, 4 blue; 4 red, 2 green; 1 blue, 1 red, 1 green; 10 red, 1 green, 5 blue"
    # print(int(get_info(text)))
    
    print(f"Sum is: {sum_possible_games(inputs)}")
    
    
    