def text_analyser():
    """
    Main function for text analysis.
    Performs the following actions:
    1. Splits the text into words.
    2. Counts the number of words with fewer than 7 characters.
    3. Finds the shortest word ending with the letter 'a'.
    4. Sorts the words by length in descending order.
    """
    text = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
    words = split_text_to_words(text)
    print("Number of words with fewer than 7 characters: ", count_words_less_7_chars(words))
    print("Shortest word ending with 'a': ", find_shortest_word_ends_a(words))
    print("List of words sorted by length in descending order: ", sort_words_descending(words))


def split_text_to_words(text):
    """
    Splits the text into words, removing commas.

    Parameters:
    text (str): The input text.

    Returns:
    list: A list of words.
    """
    return text.replace(',', ' ').split()


def count_words_less_7_chars(words):
    """
    Counts the number of words with fewer than 7 characters.

    Parameters:
    words (list): A list of words.

    Returns:
    int: The number of words with fewer than 7 characters.
    """
    counter = 0
    for word in words:
        if len(word) < 7:
            counter += 1
    return counter


def find_shortest_word_ends_a(words):
    """
    Finds the shortest word ending with the letter 'a'.

    Parameters:
    words (list): A list of words.

    Returns:
    str: The shortest word ending with 'a'.
    """
    shortest_word = words[0]
    for word in words:
        if word.lower().endswith('a'):
            if len(shortest_word) > len(word):
                shortest_word = word
    return shortest_word


def sort_words_descending(words):
    """
    Sorts the words by length in descending order.

    Parameters:
    words (list): A list of words.

    Returns:
    list: A list of words sorted by length in descending order.
    """
    words.sort(key=len, reverse=True)
    return words