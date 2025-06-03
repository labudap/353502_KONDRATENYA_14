from input_validation import int_input

def substract():
    """
    Subtracts user-input integers from an initial total of 10,000 until the total becomes negative.

    The function continuously prompts the user to input an integer, subtracts it from the total,
    and prints the current value of the total. The process stops when the total becomes negative,
    and the first negative value encountered is printed.

    The function uses `int_input` from the `input_validation` module to ensure valid integer input.
    """
    total = 10000
    print("Initial value: ", total)
    while total >= 0:
        print("Enter an integer: ")
        num = int_input()
        total -= num
        print("Current value: ", total)
    print("First negative value encountered: ", total)