

def get_words(lyrics, split_chars=(' ', ',', '.', ';', ':', '/', '_', '\n',
                                   '(', ')', '[', ']', '?', '!')):
    """
    Split text in words, splitting by a set of characters.
    :param lyrics: (str)
    :param split_chars: ([str])
    :return words: ([str])
    """
    for ch in split_chars:
        lyrics = lyrics.replace(ch, ' ')

    while '  ' in lyrics:
        lyrics = lyrics.replace('  ', ' ')

    if lyrics.startswith(' '):
        lyrics = lyrics[1:]

    if lyrics.endswith(' '):
        lyrics = lyrics[:-1]

    words = lyrics.split(' ')

    return words


def get_num_words(lyrics):
    """
    Count the number of words in a provided text.
    :param lyrics: (str)
    :return num_words: (int)
    """
    words = get_words(lyrics)
    num_words = len(words)
    return num_words


def get_unique_words(lyrics):
    """
    Extract a set with the unique words in a provided text.
    :param lyrics: (str)
    :return unique_words: (set(str))
    """
    words = get_words(lyrics)
    unique_words = set(words)
    return unique_words


def get_num_unique_words(lyrics):
    """
    Count the number of unique words in a provided text.
    :param lyrics: (str)
    :return num_unique_words: (int)
    """
    unique_words = get_unique_words(lyrics)
    num_unique_words = len(unique_words)
    return num_unique_words
