from math import sqrt, ceil
import time

def ff(time, dist):
    # first = True
    i = 0
    for v in range(time):
        if v * (time - v) > dist:
            # if first:
                # print(v)
                # first = False
            i += 1
    print(i)
    return i

def optimal_ff(time, dist):
    t1 = (time - sqrt(time * time - 4 * dist))/2
    t2 = (time + sqrt(time * time - 4 * dist))/2
    
    # print(t1)
    # print(t2)
    
    # print(ceil(t2) - int(t1) - 1)
    return ceil(t2) - int(t1) - 1

def f(times, distances):
    p = 1
    for i, time in enumerate(times):
        p *= optimal_ff(time, distances[i])
    return p

if __name__ == '__main__':
    inputs = []
    with open('input6.txt', 'r') as file:
        for line in file:
            print(line)
            if line.startswith("Time: "):
                times= [int(time) for time in line.split("Time: ")[1].strip().split()]
                print(times)
            else:
                distances = [int(time) for time in line.split("Distance: ")[1].strip().split()]
                print(distances)
                
    
    print(f"P is: {f(times, distances)}")