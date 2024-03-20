import re

def gcd(a, b):
    """Calculate the greatest common divisor using Euclid's algorithm."""
    
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Calculate the least common multiple using the formula LCM(a, b) = |a * b| / GCD(a, b)."""
    
    return abs(a * b) // gcd(a, b)

def lcm_of_list(numbers):
    """Calculate the least common multiple for a list of numbers."""
    
    result = 1
    for num in numbers:
        result = lcm(result, num)
    return result

def num_of_steps(start_words, instructions, words):
    """"Calculate the number of steps required to get from all start words to words that ends with 'Z' in the same step."""
    
    num_of_steps_for_all_start_words = []
    for start_word in start_words:
        num_of_steps = num_of_steps_for_word(start_word, instructions, words)
        num_of_steps_for_all_start_words.append(num_of_steps)

    return lcm_of_list(num_of_steps_for_all_start_words)

def num_of_steps_for_word(start_word, instructions, words):
    """"Calculate the number of steps required to get from start word to word that ends with 'Z'."""
    
    n = len(instructions)
    step_num = 0
    i = 0
    current_word = start_word
    
    while i < n:
        if instructions[i] == 'L':
            next_word = words[current_word][0]
        else:
            next_word = words[current_word][1]
        
        step_num += 1
        # print(f"{step_num}. Go from {current_word} {instructions[i]} to {next_word}")

        current_word = next_word
        i += 1
        
        if current_word.endswith('Z'):
            return step_num
        
        if i == n:
            # repeat
            i = 0

if __name__ == '__main__':
    words = dict()
    words_that_end_with_A = []
    first = True
    with open('input8.txt', 'r') as file:
        for line in file:
            if first:
                instructions = line.strip()
                first = False
            else:
                pattern = r'(\w+) = \((\w+), (\w+)\)'
                match = re.match(pattern, line)
                if match:
                    word, left_word, right_word = match.groups()
                    word_instruction = (left_word, right_word)
                    if word.endswith('A'):
                        words_that_end_with_A.append(word)
                    words[word] = word_instruction

    print(f"Num of steps: {num_of_steps(words_that_end_with_A, instructions, words)}")
