from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from random import random
from itertools import product
from copy import deepcopy


def parse_songwriters(text):
    """
    Obtain names of songwriters from the provided website text.
    :param text: (str) songwriters part of text extracted from webpage.
    :return songwriters: set(str) each element of the set is a songwriter.
    """
    # structure of input text: "Songwriter(s): <sw1>, <sw2>, ..."
    # split songwriters text by comma:
    try:
        songwriters_txt = text.split(':')[1].replace('\n', '')
        songwriters_raw_list = songwriters_txt.split(',')
    except IndexError:
        songwriters_raw_list = []
        print('Failed to parse songwriters from text: {}'.format(text))

    # clean spaces at the start or end of songwriter string & add to final set:
    songwriters = set()
    for sw in songwriters_raw_list:

        while sw[0] == ' ':
            sw = sw[1:]
        while sw[-1] == ' ':
            sw = sw[:-1]

        if not sw:
            continue

        songwriters.add(sw)

    return songwriters


def clean_sw(sw):
    """
    Clean songwriter name: apply lowercase, replace '.' and '-' by spaces,
    remove double spaces and spaces at the start and/or end of name.
    :param sw: (str) songwriter name.
    :return sw: (str) cleaned songwriter name.
    """
    sw = sw.lower()

    sw = sw.replace('.', ' ').replace('-', ' ')

    while '  ' in sw:
        sw = sw.replace('  ', ' ')

    if sw[0] == ' ':
        sw = sw[1:]

    if sw[-1] == ' ':
        sw = sw[:-1]

    return sw


def unify_songwriters(raw_songwriters):
    """
    Given a list of full names ("raw_songwriters"), this function aims to
    detect full names that are slightly different but which refer to the same
    person.
    In order to do so, it converts all the full names to lowercase, and it
    removes stop characters ('.').
    Then it compares the resulting songwriter names between them word by word,
    splitting each by space (' '), and ignoring word order.
    Conditions to assume that 2 songwriter names refer to the same person:
    - If all the words in one songwriter are contained in the other songwriter,
      then these songwriters are considered to be the same:
      e.g.: "lennon" / "john lennon"
      e.g.: "lennon john" / "john w lennon"
    - If all the words in one songwriter are contained in the other songwriter,
      except for some words, but these words match the beginnings of remaining
      words in the other songwriter, then the songwriters are considered as the
      same:
      e.g. "johnny lennon" / "lennon john"
      e.g. "j w lennon" / "john lennon"
    :param raw_songwriters: ([str]) iterable containing names of songwriters.
    :return equivalences: {str->str} relates old songwriter names to discard
        to the songwriter name it should be replaced by.
    """
    change_in_songwriters = True
    equivalences = {}

    while change_in_songwriters:

        change_in_songwriters = False

        # analyse all combinations of songwriters to compare with each other:
        for sw_1, sw_2 in product(raw_songwriters, raw_songwriters):

            # skip comparison of songwriter with itself:
            if sw_1 == sw_2:
                continue

            # compare words in both songwriters in all lowercase, skipping
            # stops ('.') and replacing dashes ('-') by spaces:
            words_1 = clean_sw(sw_1).split(' ')
            words_2 = clean_sw(sw_2).split(' ')

            # for each word in words 1, check if it is contained in words 2
            # and if it is, then discard word from words 1 and words 2 lists:
            change_in_words = True
            while change_in_words:
                change_in_words = False
                for w_1 in list(words_1):
                    if w_1 in words_2:  # "john" <-> "john"
                        # word 1 is contained in words 2 list: remove both from
                        # their respect. lists and go back to beginning of loop:
                        words_1.remove(w_1)
                        words_2.remove(w_1)
                        change_in_words = True
                        break

            # for each word in words 1, check if its initial characters are
            # contained in words 2, and they are, then discard the word from
            # words 1 list and the initials from words 2 list:
            change_in_words = True
            while change_in_words:
                change_in_words = False
                for w_1 in list(words_1):
                    # check if initial sequence of word is contained in words 2:
                    for i in range(len(w_1)):  # initial seq of any length
                        if w_1[:i+1] in words_2:  # "john" <-> "johnny"
                            # word 1 start is contained in word 2: remove both
                            # from lists and go back to beginning of loop:
                            words_1.remove(w_1)
                            words_2.remove(w_1[:i+1])
                            change_in_words = True
                            break
                    if change_in_words:
                        break

            # if now at least one words list is empty, then the conditions have
            # been matched, and we consider that both songwriter names refer
            # to the same person:
            if not words_1 or not words_2:
                # keep the shortest songwriter name:
                if len(sw_1) < len(sw_2):
                    equivalences[sw_2] = sw_1
                    raw_songwriters.remove(sw_2)
                else:
                    equivalences[sw_1] = sw_2
                    raw_songwriters.remove(sw_1)
                # a songwriter has been discarded, back to beginning of loop:
                change_in_songwriters = True
                break

    change = True
    while change:
        change = False
        for sw, eq in equivalences.items():
            if eq in equivalences:
                equivalences[sw] = equivalences[eq]
                change = True
                break

    return equivalences


def unify_songs_songwriters(songs):
    """
    Given a set of songs with their songwriters attributes, this function
    iterates over all the songwriters of all the songs and creates a set of
    all unique songwriter names.
    Then it calls "unify_songwriters" function passing as an argument all these
    songwriter names in order to obtain a simplified set of songwriters,
    detecting all those that are duplicate under slightly different names.
    Then it modifies the songwriter attributes of the songs according to this
    simplified set of songwriter names.
    :param songs: {str->Song object} dictionary in which the keys are song
        titles and the values are the corresponding Song objects.
    """
    # Load all different songwriter strings in all songs:
    raw_songwriters = set()
    for song in songs.values():
        for sw in song.songwriters:
            raw_songwriters.add(sw)

    # find out repetitions of songwriters and obtain equivalences dictionary
    # to unify all names that refer to the same person:
    equivalences = unify_songwriters(raw_songwriters)
    print('Raw songwriters: {}'.format(raw_songwriters))
    print('Songwriter equivalences found: {}'.format(equivalences))

    # Replace the songwriters in the songs by their equivalent songwriters:
    for song in songs.values():
        old_songwriters = deepcopy(song.songwriters)
        song.songwriters = set()
        for sw in old_songwriters:
            if sw in equivalences:
                eq_sw = equivalences[sw]
            else:
                eq_sw = sw
            song.songwriters.add(eq_sw)


def scrape_lyrics_azlyrics(lyrics_url, chromedriver_path, headless=True,
                           error_count=0):
    """
    Given a URL to the lyrics of a song in azlyrics, this function parses the
    lyrics from it and the songwriters if available, and returns both values.
    :param lyrics_url: (str) URL to the azlyrics song lyrics webpage.
    :param chromedriver_path: (str) path to the chromedriver executable file.
    :param headless: (boolean) if set as False the browser window will be shown,
        otherwise, it will not.
    :param error_count: (integer) starts at 0. If an error occurs, it is escaped
        and the scraping is retried (the function is recalled). The process is
        retried a maximum of 5 times, then the error is raised.
    :return lyrics: (str) lyrics of the song.
    :return songwriters: set(str) each element of the set is a songwriter.
    """
    try:
        # initialise chromedriver and load song lyrics webpage:
        options = Options()
        if headless:
            options.add_argument("--headless")  # to not see browser window
        driver = webdriver.Chrome(chromedriver_path, options=options)
        driver.get(lyrics_url)

        # search for main frame of webpage:
        main_frame = driver.find_element_by_xpath(
            "//div[@class='col-xs-12 col-lg-8 text-center']")
        main_frame_elements = main_frame.find_elements_by_xpath(".//*")

        # search for lyrics element in main frame:
        next_element_are_lyrics = False
        prev_element_was_br = False
        lyrics_found = False
        songwriters = set()

        for el in main_frame_elements:

            if lyrics_found:  # lyrics already found, here we look for writers
                if el.tag_name == 'div' and el.text.startswith('Writer(s):'):
                    songwriters = parse_songwriters(el.text)
                continue

            if next_element_are_lyrics and el.tag_name == 'div':  # lyrics here
                lyrics = el.text
                lyrics_found = True

            if el.tag_name == 'br':
                if prev_element_was_br:  # element before lyrics located
                    next_element_are_lyrics = True
                prev_element_was_br = True

        # close chromedriver:
        driver.close()

    # escape errors and retry a maximum of 5 times:
    except BaseException as e:
        if error_count > 5:  # max number of errors reached: raise error
            print('Error when scraping song. Max errors escaped reached.')
            raise e
        # wait 10-50 seconds and try again:
        time.sleep(10 * error_count)
        print('Error when scraping song at URL {}:'.format(lyrics_url), e)
        print('Retrying...')
        lyrics, songwriters = \
            scrape_lyrics_azlyrics(lyrics_url, chromedriver_path,
                                   headless=headless, error_count=error_count+1)

    return lyrics, songwriters


def scrape_lyrics_songs_azlyrics(songs, chromedriver_path, headless=True,
                                 wait_seconds=15):
    """
    Iterate over a series of songs and launch "scrape_lyrics_azlyrics" function
    for each of them in order to find their lyrics and songwriters from their
    respective azlyrics websites. Add resulting lyrics and songwriters to the
    songs' attributes.
    :param songs: {str->Song object} dictionary in which the keys are song
        titles and the values are the corresponding Song objects.
    :param chromedriver_path: (str) path to the chromedriver executable file.
    :param headless: (boolean) if set as False the browser window will be shown,
        otherwise, it will not.
    :param wait_seconds: (int) number of max seconds to wait between consecutive
        lyrics searches in order to avoid being denied access to website. The
        actual number of seconds waited between searches is a random number
        between 0 and this value.
    """
    for song in songs.values():

        # skip instrumental songs (no lyrics):
        if song.instrumental:
            song.lyrics = ''
            continue

        # wait random time to avoid being denied access to website:
        time.sleep(wait_seconds * random())

        # scrape lyrics and save them to 'lyrics' attribute of song object
        # if found, do the same with songwriters:
        song.lyrics, song.songwriters = \
            scrape_lyrics_azlyrics(song.lyrics_url, chromedriver_path,
                                   headless=headless)

        print('lyrics scraped for song: "{}"'.format(song.title))

    # unify songwriters who may appear under different names
    # e.g. John Lennon / Lennon John W. / J W Lennon / ...
    unify_songs_songwriters(songs)
