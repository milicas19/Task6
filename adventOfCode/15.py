MUL = 17
DIV = 256

def code(word):
    result = 0
    for char in word:
        ascii_code = ord(char)
        result += ascii_code
        result = (result * MUL) % DIV
    return result
        

if __name__ == '__main__':
    file_name = 'input15.txt'
    result = 0
    map = dict()
    boxes_i = [0 for _ in range(256)]
    
    with open(file_name, 'r') as file:
        index = 0
        for line in file:
            word = line.strip()
            if "-" in word:
                [label, num] = word.split("-")
                map[label] = [-1, index]
            else:
                [label, num] = word.split("=")
                if label in map and map[label][0] != -1:
                    # change just the focal length
                    map[label][0] = int(num)
                else:
                    map[label] = [int(num), index]
            index += 1
    
    
    # print(map)
    result = 0
    for label, [num, ind] in sorted(map.items(), key=lambda x: x[1][1]):
        if num == -1:
            continue
        else:
            box_num = code(label)
            boxes_i[box_num] += 1
            
            label_res = (box_num + 1) * boxes_i[box_num] * num
            # print(label_res)
            result += label_res
    
    print(f"Result is: {result}")