# import time
# import psutil
from pyperf import Runner
from scipy.special import comb


############################ GET RIGHT-MOST ELEMENT ############################
def get_right_most_element(numbers):
    """
    This function determines the rightmost element in a list numbers.
    
    e.g numbers = [5  10  13  16  21  30  45], rightmost element is 68
    
        10  13  16  21  30  45  68
           3   3   5   9  15  23
             0   2   4   6   8
               2   2   2   2
                 0   0   0
    """
    new_numbers = []
    num_of_same = 0
    lasts = []
    i = 0
    
    while i < len(numbers) - 1:
        new_numbers.append(numbers[i + 1] - numbers[i])
        if numbers[i + 1] == numbers[i]:
            num_of_same += 1
            
        i += 1
        
        if i == len(numbers) - 1:
            # saving last elements of each line, so we can calculate the rightmost element
            lasts.append(numbers[i])
            # if all numbers in the line aren't the same, 
            # then we continue to calculate next line till we reach all the same numbers
            if num_of_same != len(numbers) - 1:
                i = 0
                num_of_same = 0
                numbers = new_numbers
                new_numbers = []
                
    # calculating rightmost element by adding all numbers from the list lasts            
    result = 0
    for last in lasts:
        result += last
    return result

############################ GET LEFT-MOST ELEMENT ############################
def subtract_list(numbers):
    """
    This function calculates a series of subtractions within the list numbers. 
    
    e.g numbers = [10, 2, 4, 6], 
    the result would be 10 - (2 - (4 - 6)) = 10 - (2 - (4 - (6 - 0))) = 6
    """
    n = len(numbers)
    
    if n == 1:
        return numbers[0]
    
    result = 0
    for i in range(n - 1, -1, -1):
        result = numbers[i] - result
    
    return result

def get_left_most_element(numbers):
    """
    This function determines the leftmost element in a list numbers.
    
    e.g numbers = [5  10  13  16  21  30  45], leftmost element is 5
    
        5  10  13  16  21  30  45
          5   3   3   5   9  15
           -2   0   2   4   6
              2   2   2   2
                0   0   0
    """
    new_numbers = []
    num_of_same = 0
    firsts = []
    i = 0
    
    while i < len(numbers) - 1:
        new_numbers.append(numbers[i + 1] - numbers[i])
        if numbers[i + 1] == numbers[i]:
            num_of_same += 1
        i += 1
        if i == len(numbers) - 1:
            # saving first elements of each line, so we can calculate the leftmost element
            firsts.append(numbers[0])
            # if all numbers in the line aren't the same, 
            # then we continue to calculate next line till we reach all the same numbers 
            if num_of_same != len(numbers) - 1:
                i = 0
                num_of_same = 0
                numbers = new_numbers
                new_numbers = []
                
    return subtract_list(firsts)

############################ GET LEFT-MOST ELEMENT USING BINOMIAL COEFFICIENTS ############################
def get_alternating_binomial_coefficient(n, k):
    """This function calculates b(n, k) = (-1)^k * (n - 1)* ... * (n - k + 1)/k * (k - 1) * ... * 2"""
    return (-1)**k * comb(n, k, exact=True) 

def get_left_most_element_using_bin_coef(numbers):
    """
    This function determines the leftmost element in a list numbers using binomial coefficients.
    (memory optimization - without list, but we still have list for numbers so maybe it's not that optimal)
    
    e.g numbers = [5  10  13  16  21  30  45], leftmost element is 5
    
        5  10  13  16  21  30  45
          5   3   3   5   9  15
           -2   0   2   4   6
              2   2   2   2
                0   0   0
    """
    n = len(numbers)
    result = 0
    
    for i in range(n - 1, 0, -1):
        line_result = 0
        k = 0
        for j in range(i, -1, -1):
            line_result += numbers[j] * get_alternating_binomial_coefficient(i, k)
            k += 1
            
        result = line_result - result
    
    result = numbers[0] - result
    return result

############################ MAIN FUNCTION ############################
def sum_of_elements(list_of_numbers, type_of_element = 'rightmost'):
    """
    This function adds up all the rightmost/leftmost elements of numbers from the list of numbers.
    """
    result = 0
    
    if type_of_element == 'rightmost':
        for numbers in list_of_numbers:
            result += get_right_most_element(numbers)
    elif type_of_element == 'leftmost':
        for numbers in list_of_numbers:
            result += get_left_most_element(numbers)
    else:
        print("type_of_element parameter must be 'leftmost' or 'rightmost'" )
        return None
    
    return result


if __name__ == '__main__':
    list_of_numbers = []
    with open('input9.txt', 'r') as file:
        for line in file:
            numbers = [int(num) for num in line.split()]
            list_of_numbers.append(numbers)
    type_of_element='leftmost'
    # start_time = time.time()
    # cpu_before = psutil.cpu_percent(interval=1)
    # mem_before = psutil.virtual_memory().used
    runner = Runner()
    runner.bench_func("sum_of_elements", sum_of_elements, [[10, 13, 16, 21, 30, 45]], 'leftmost')
    result = runner.run()
    # Check the results
    #assert result.get_result("sum_leftmost").mean < result.get_result("sum_all").mean, "Leftmost sum should be faster than summing all elements"

    # Display the results
    print(result)
    
    #print(f"Sum of rightmost elements: {sum_of_elements(list_of_numbers)}")
    #print(f"Sum of leftmost elements: {sum_of_elements(list_of_numbers, type_of_element='leftmost')}")

    # end_time = time.time()
    # cpu_after = psutil.cpu_percent(interval=1)
    # mem_after = psutil.virtual_memory().used

    # print(f"Elapsed time: {end_time - start_time} seconds")
    # print(f"CPU usage: {cpu_after - cpu_before}%")
    # print(f"Memory usage: {mem_after - mem_before} bytes")
