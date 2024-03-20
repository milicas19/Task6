from collections import deque

def f(seeds, inputs):
    min_location = 0
    first = True
    for pos, (seed, seed_len) in enumerate(seeds):
        # print(f"Progress: {pos}")
        sources = [(seed, seed_len)]
        q = deque()
        for i, value_list in inputs.items():
            # print(f"Progress {i}")
            new_sources = []
            for (source, source_len) in sources:
                q.append((source, source_len))
                for (dest_start, source_start, n) in value_list:
                    # print(q)
                    if not q:
                        break
                    (source, source_len) = q.popleft()
                    q.append((source, source_len))
                    # print(f"{source} {source_len}")
                    # print(f"{dest_start} {source_start} {n}")
                    
                    # case 1
                    if (source_start < source and source_start + n - 1 < source) or source_start > source + source_len - 1:
                        continue
                    # case 2
                    elif source_start >= source and source_start + n <= source + source_len:
                        new_sources.append((dest_start, n))
                        q.pop()
                        if source_start != source:
                            q.append((source, source_start - source))
                        if source_start + n != source + source_len:
                            q.append((source_start + n, source + source_len - source_start - n))
                    # case 3
                    elif source_start < source and source_start + n > source + source_len:
                        new_sources.append((source + dest_start - source_start, source_len))
                        q.pop() 
                    # case 4
                    elif source_start < source and source_start + n - 1 >= source and source_start + n <= source + source_len:
                        new_sources.append((source + dest_start - source_start, source_start + n - source))
                        q.pop()
                        if source + source_len - (source_start + n) != 0:
                            q.append((source_start + n, source + source_len - (source_start + n)))
                    # case 5
                    elif source_start <= source + source_len - 1 and source_start >= source and source_start + n > source + source_len:
                        new_sources.append((dest_start, source + source_len - source_start))
                        q.pop()
                        if source_start != source:
                            q.append((source, source_start - source))
                        
                while q:
                    (source, source_len) = q.pop()
                    new_sources.append((source, source_len))
                
                # print(new_sources)
            
            sources = new_sources
            # print(sources)
        
        for (source, _) in sources:
            if first:
                min_location = source
                first = False
            elif min_location > source:
                min_location = source
                
    return min_location

if __name__ == '__main__':
    seeds = []
    inputs = dict()
    i = 0
    with open('input5.txt', 'r') as file:
        for line in file:
            if line.startswith("seeds"):
                seed_line = line.split("seeds:")
                seeds_str = seed_line[1].strip().split()
                # print(seeds_str)
                seeds = [(int(seeds_str[i]), int(seeds_str[i + 1])) for i in range(0, len(seeds_str), 2)]
                # print(seeds)
            elif line.strip() != "" and not any(char.isdigit() for char in line):
                i += 1
                inputs[i] = []
            elif line.strip() != "":
                num_line = line.split()
                nums = (int(num_line[0]), int(num_line[1]), int(num_line[2]))
                inputs[i].append(nums)
    
    print(f"Min is: {f(seeds, inputs)}")