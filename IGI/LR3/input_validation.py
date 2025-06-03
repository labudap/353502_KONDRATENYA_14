

def int_input():
    """
    Prompts the user to input an integer and ensures the input is valid.

    The function continuously prompts the user until a valid integer is entered.
    If the input is not a valid integer, an error message is displayed.

    Returns:
    int: The valid integer entered by the user.
    """
    while True:
        num = input()
        try:
            int(num)
            return int(num)
        except ValueError:
            print("Enter a valid integer!")


def float_input():
    """
    Prompts the user to input a floating-point number and ensures the input is valid.

    The function continuously prompts the user until a valid floating-point number is entered.
    If the input is not a valid floating-point number, an error message is displayed.

    Returns:
    float: The valid floating-point number entered by the user.
    """
    while True:
        num = input()
        try:
            float(num)
            return float(num)
        except ValueError:
            print("Enter a valid floating-point number!")