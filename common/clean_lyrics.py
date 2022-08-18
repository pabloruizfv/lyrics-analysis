import nltk
from nltk import word_tokenize
from random import shuffle, seed


SPLIT_WORD_CHARS = {' ', '\n', ',', '.', ';', ':', '/', '_',
                    '(', ')', '[', ']', '{', '}', '?', '!'}


def apply_lowercase(lyrics):
    """
    Given some lyrics, this function converts all letters to lowercase except
    for those uppercase letters that are followed and/or preceded by another
    uppercase letter (i.e. acronyms: "USA", etc.), and "I" pronouns.
    :param lyrics: (str)
    :return lowered_lyrics: (str)
    """
    # if we did not add these chars, then we would mistakenly convert '"USA"'
    # to '"usa"':
    split_word_chars = SPLIT_WORD_CHARS | {'\"', '\'', '’'}

    lowered_lyrics = ''

    for i, ch in enumerate(lyrics):

        # load next and previous character:
        if i == 0:  # first character
            previous_ch = ' '  # split word character
        else:
            previous_ch = lyrics[i-1]

        if i == len(lyrics) - 1:  # last character
            next_ch = ' '  # split word character
        else:
            next_ch = lyrics[i+1]

        # decide whether or not to lower an uppercase character:
        if ch.lower != ch:  # uppercase ("A")
            if previous_ch in split_word_chars:  # (" A")
                if next_ch.lower() != next_ch:  # uppercase too (" AB")
                    lowered_lyrics += ch
                elif ch == 'I' and next_ch in split_word_chars:  # (" I ")
                    lowered_lyrics += ch
                else:  # (" Ab")
                    lowered_lyrics += ch.lower()

            elif previous_ch.lower() != previous_ch:  # uppercase too ("BA")
                lowered_lyrics += ch

            else:  # weird case ("bA")
                lowered_lyrics += ch.lower()

        elif ch in split_word_chars:  # split character (" ")
            lowered_lyrics += ch

        else:  # lowercase ("a")
            lowered_lyrics += ch

    return lowered_lyrics


def filter_pos(lyrics, pos_tags):
    """
    Given some lyrics, this function keeps only those words in the lyrics with
    part-of-speech tags contained in the given tag iterable.
    :param lyrics: (str)
    :param pos_tags: iterable(str)
    :return filtered_lyrics: (str)
    """
    seed(10)
    words = []
    text = word_tokenize(lyrics)
    for word, tag in nltk.pos_tag(text):
        if word == 'starman':
            tag = 'NN'
        if tag in pos_tags:
            words.append(word)
    shuffle(words)
    while 'n\'t' in words:
        words.remove('n\'t')
    filtered_lyrics = ' '.join(words)
    return filtered_lyrics


def remove_stopwords(lyrics, stopwords, numbers=True):
    """
    Remove stopwords from the given lyrics.
    :param lyrics: (str)
    :param stopwords: ([str])
    :param numbers: (boolean)
    :return filtered_lyrics: (str)
    """
    words = []
    text = word_tokenize(lyrics)
    for word, _tag in nltk.pos_tag(text):

        if numbers is True:
            try:
                int(word)
            except ValueError:
                if '0' in word:
                    print('-{}-'.format(word))
                if word not in stopwords:
                    words.append(word)
        else:
            if word not in stopwords:
                words.append(word)

    filtered_lyrics = ' '.join(words)
    return filtered_lyrics
