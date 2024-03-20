
def f(inputs):
    sum = 0
    copies = [1 for _ in range(len(inputs))]
    
    for i, input in enumerate(inputs):
        print(i)
        match_num = ff(input)
        print(f"match_num={match_num}")
        for j in range(i + 1, i + match_num + 1):
            copies[j] += copies[i]
    
    print(copies)
    for copy in copies:
        sum += copy
    return sum

def ff(input):
    step = 0
    parts = input.split('|')
    print(parts)
    winning = set(parts[0].strip().split())
    available = parts[1].strip().split()
    
    print(winning)
    print(available)

    for a in available:
        if a in winning:
            step += 1
    
    return step


if __name__ == '__main__':
    inputs = []
    with open('input4.txt', 'r') as file:
        for line in file:
            parts = line.split(':')
            if len(parts) !=2:
                print("Error !!!")
            input = parts[1]
            inputs.append(input)
            
    print(f"Sum is: {f(inputs)}")
