import re

def calc_sum(lines):
    m = len(lines[0])
    sum = 0
    above_line = ""
    below_line = ""
    n = len(lines)
    for i in range(n):
        line = lines[i]
        if i == 0:
            above_line = '.' * m
        else:
            above_line = lines[i - 1]
        if i == n - 1:
            below_line = '.' * m
        else:
            below_line = lines[i + 1]
        
        print(above_line)
        print(line)
        print(below_line)
        
        sum += geer_line(above_line, line, below_line)
    
    return sum

def calc_sum_of_line(above_line, line, below_line):
    sum = 0
    pattern = r'\b\d+\b'

    matches = [(match.start(), match.end(), match.group()) for match in re.finditer(pattern, line)]
    
    print(matches)
    
    for (s, e, num) in matches:
        print(f"s={s}, e={e}, num={num}")
        sum += valid_num(s, e, num, line, above_line, below_line)
    
    print(f"sum={sum}")
    return sum

def valid_num(s, e, num, line, above_line, below_line):
    if s > 0:
        c1 = line[s - 1]
        c2 = above_line[s - 1]
        c3 = below_line[s - 1]
        if (not c1.isdigit() and c1 != '.') or (not c2.isdigit() and c2 != '.') or (not c3.isdigit() and c3 != '.'):
            return int(num)
    if e < len(line):
        c1 = line[e]
        c2 = above_line[e]
        c3 = below_line[e]
        if (not c1.isdigit() and c1 != '.') or (not c2.isdigit() and c2 != '.') or (not c3.isdigit() and c3 != '.'):
            return int(num)
    for i in range(s, e):
        c1 = above_line[i]
        c2 = below_line[i]
        if (not c1.isdigit() and c1 != '.') or (not c2.isdigit() and c2 != '.'):
            return int(num)

    return 0

def geer_line(above_line, line, below_line):
    mapa = dict()
    pattern = r'\b\d+\b'

    line_matches = [(match.start(), match.end(), match.group()) for match in re.finditer(pattern, line)]
    aline_matches = [(match.start(), match.end(), match.group()) for match in re.finditer(pattern, above_line)]
    bline_matches = [(match.start(), match.end(), match.group()) for match in re.finditer(pattern, below_line)]
    
    for (s, e, num) in line_matches:
        if s > 0:
            pos = s - 1
            c = line[s - 1]
            if c == '*':
                if pos in mapa:
                    mapa[pos].append(int(num))
                else:
                    mapa[pos] = [int(num)]
        if e < len(line):
            c = line[e]
            if c == '*':
                if e in mapa:
                    mapa[e].append(int(num))
                else:
                    mapa[e] = [int(num)]
                    
    for (s, e, num) in aline_matches:
        if s > 0:
            pos = s - 1
            c = line[s - 1]
            if c =='*':
                if pos in mapa:
                    mapa[pos].append(int(num))
                else:
                    mapa[pos] = [int(num)]
        if e < len(line):
            c = line[e]
            if c == '*':
                if e in mapa:
                    mapa[e].append(int(num))
                else:
                    mapa[e] = [int(num)]
        for i in range(s, e):
            c = line[i]
            if c == '*':
                if i in mapa:
                    mapa[i].append(int(num))
                else:
                    mapa[i] = [int(num)]
                    
    for (s, e, num) in bline_matches:
        if s > 0:
            pos = s - 1
            c = line[s - 1]
            if c =='*':
                if pos in mapa:
                    mapa[pos].append(int(num))
                else:
                    mapa[pos] = [int(num)]
        if e < len(line):
            c = line[e]
            if c == '*':
                if e in mapa:
                    mapa[e].append(int(num))
                else:
                    mapa[e] = [int(num)]
        for i in range(s, e):
            c = line[i]
            if c == '*':
                if i in mapa:
                    mapa[i].append(int(num))
                else:
                    mapa[i] = [int(num)]
    print(mapa)
    
    sum = 0
    for values in mapa.values():
        n = len(values)
        if n > 1:
            for i in range(n - 1):
                for j in range(i + 1, n):
                    print(values[i])
                    print(values[j])
                    sum += values[i] * values[j]
    
    print(sum)
    return sum
    
    #star_positions = [match.start() for match in re.finditer(r'\*', line)]
    
    
    
    
    
    

if __name__ == '__main__':
    inputs = []
    with open('input3.txt', 'r') as file:
        for line in file:
            line = line.strip()
            inputs.append(line)
            
    print(f"Sum is: {calc_sum(inputs)}")
    
    # text = "Game 12: 10 red, 2 green, 4 blue; 4 red, 2 green; 1 blue, 1 red, 1 green; 10 red, 1 green, 5 blue"
    # print(int(get_info(text)))
    
    # print(f"Sum is: {sum_possible_games(inputs)}")