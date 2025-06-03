from input_validation import int_input
from list_initialyser import user_initializer
from list_initialyser import random_initializer

def analys_list():
    """
    Analyzes a list based on user-selected initialization method.

    The function allows the user to choose between manual initialization or random generation of a list.
    It then finds the minimum negative value in the list and calculates the sum of elements between
    the first and second negative values. The results are printed to the console.
    """
    print("Choose the list initialization method:\n"
          "1. Manual initialization\n"
          "2. Generate a list of a specified length")
    while True:
        chosen_way = int_input()
        if chosen_way == 1 or chosen_way == 2:
            break
        print("Enter a valid value!")
    match chosen_way:
        case 1:
            array = list(user_initializer())
        case 2:
            array = list(random_initializer())
    print_array(array)
    min_negative = find_min_negative(array)
    if min_negative == 0:
        print("The list contains no negative values")
    else:
        print("The minimum negative element in the list: ", min_negative)
    sum = find_sum_between_negatives(array)
    if sum == -1:
        print("The list contains fewer than 2 negative values")
    else:
        print("Sum of elements between the first and second negative values: ", sum)


def find_min_negative(array):
    """
    Finds the minimum negative value in the list.

    Parameters:
    array (list): The list of numbers to search.

    Returns:
    float: The minimum negative value. Returns 0 if no negative values are found.
    """
    min = 0
    for num in array:
        if num < 0 and num < min:
            min = num
    return min


def print_array(array):
    """
    Prints the contents of the list.

    Parameters:
    array (list): The list of numbers to print.
    """
    print("Your list: ", array)


def find_sum_between_negatives(array):
    """
    Calculates the sum of elements between the first and second negative values in the list.

    Parameters:
    array (list): The list of numbers to analyze.

    Returns:
    float: The sum of elements between the first and second negative values.
           Returns -1 if there are fewer than 2 negative values in the list.
    """
    neg_number = 0
    sum = 0
    for num in array:
        if num < 0:
            neg_number += 1
            if neg_number == 1:
                continue
        if neg_number == 1:
            sum += num
            continue
        if neg_number == 2:
            return sum
    sum = -1
    return sum