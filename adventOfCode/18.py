import re

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
DIR_MAP = {'R': (0, 1)}
def get_cube_num(instructions, start = (0, 0)):
    for instr in instructions:
        

if __name__ == '__main__':
    instructions = []
    pattern = r'([DLRU]) (\d+) \((\S+)\)'
    file_name = 'input181.txt'
    
    with open(file_name, 'r') as file:
        for line in file:
            row = line.strip()
            match = re.match(pattern, row)

            if match:
                letter = match.group(1)
                number = match.group(2)
                rgb_color = match.group(3)
                
                instructions.append((letter, int(number), rgb_color))
