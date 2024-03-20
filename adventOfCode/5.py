pr = 1000000
prr = 1000000

def f(seeds, inputs):
    min_location = 0
    first = True
    for seed in seeds:
        source = seed
        for _, value_list in inputs.items():
            for (dest_start, source_start, n) in value_list:
                if source >= source_start and source < source_start + n:
                    source = dest_start + source - source_start
                    break
        if first:
            min_location = source
            first = False
        elif source < min_location:
            min_location = source
    
    return min_location

def ff(seed, inputs):
    source = seed
    for _, value_list in inputs.items():
        for (dest_start, source_start, n) in value_list:
            if source >= source_start and source < source_start + n:
                print(f"source={source} source_start={source_start}")
                source = dest_start + source - source_start
                break

    return source

if __name__ == '__main__':
    seeds = []
    inputs = dict()
    i = 0
    with open('input5.txt', 'r') as file:
        for line in file:
            if line.startswith("seeds"):
                seed_line = line.split("seeds:")
                seeds_str = seed_line[1].strip().split()
                print(seeds_str)
                seeds = [(int(seeds_str[i]), int(seeds_str[i + 1])) for i in range(0, len(seeds_str), 2)]
                print(seeds)
            elif line.strip() != "" and not any(char.isdigit() for char in line):
                i += 1
                inputs[i] = []
            elif line.strip() != "":
                num_line = line.split()
                nums = (int(num_line[0]), int(num_line[1]), int(num_line[2]))
                inputs[i].append(nums)
    
    
    min_location = 0
    skup = set()
    first = True
    for j, (seed, n) in enumerate(seeds):
        print(f"{j}")
        for i in range(n):
            if i % pr == 0:
                print(f"Progress {i}/{n}")
                
            if(seed+i) not in skup:
                skup.add(seed+i)
                s = ff(seed + i, inputs)
            
                if first:
                    min_location = s
                    first = False
                elif s < min_location:
                    min_location = s

    print(f"Min is: {min_location}")