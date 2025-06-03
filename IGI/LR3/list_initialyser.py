from input_validation import int_input, float_input
import random

def user_initializer():
    """
    Generator that yields user-provided floating-point numbers one by one.
    
    Prompts the user to specify the total number of elements, then sequentially
    requests each element through console input.
    
    Yields:
        float: The next user-provided number in the sequence.
        
    Usage Examples:
        # Get all numbers at once as a list
        >>> numbers = list(user_initializer())
        
        # Process numbers as they're entered
        >>> for num in user_initializer():
        ...     process_number(num)
    """
    print("Enter the number of elements in the list: ")
    count = int_input()
    for i in range(count):
        print(f"Enter the element at index {i}:")
        yield float_input()

def random_initializer():
    """
    Generator that yields random floating-point numbers between -100 and 100.
    
    Prompts the user to specify the total number of elements, then generates
    random numbers in the specified range.
    
    Yields:
        float: The next randomly generated number in the sequence (-100 ≤ x ≤ 100).
        
    Usage Examples:
        # Get all random numbers at once
        >>> random_nums = list(random_initializer())
        
        # Process numbers as they're generated
        >>> for num in random_initializer():
        ...     analyze(num)
    """
    print("Enter the number of elements in the list: ")
    count = int_input()
    for _ in range(count):
        yield random.uniform(-100, 100)