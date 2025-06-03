def space_comma_counter():
    """
    Counts the number of spaces and commas in a given text input by the user.

    The function prompts the user to input a text, then iterates through each character
    in the text to count the number of spaces and commas. It returns the counts of spaces
    and commas as a tuple.

    Returns:
    tuple: A tuple containing two integers:
        - The first integer is the count of spaces.
        - The second integer is the count of commas.
    """
    text = input("Enter text: ")
    comma_counter = 0
    space_counter = 0
    for char in text:
        if char.isspace():
            space_counter += 1
        if char == ',':
            comma_counter += 1
    return space_counter, comma_counter