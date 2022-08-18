from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import re
from common.songs_and_albums import Song, Album


def parse_song_text(song_text):
    """
    Obtain name of song, and whether it is instrumental or not from the
    provided website text.
    :param song_text: (str) this song's part of text extracted from webpage.
    :return title: (str) title of the song.
    :return instrumental: (boolean) whether the song is instrumental or not.
    """
    # Replace line breaks by spaces:
    title = song_text.replace('\n', ' ')

    # if the song is instrumental, it is indicated in the text:
    instrumental = '(Instrumental)' in song_text
    # Remove '(Instrumental)' string from song title:
    if instrumental:
        title = title.replace('(Instrumental)', '').replace('\n', '')

    return title, instrumental


def parse_album_text(album_text):
    """
    Obtain name of album and its year and album type from the website text.
    Create Album object and add 'number' attributes too.
    :param album_text: (str) this album's part of text extracted from webpage.
    :return title: (str) album title.
    :return year: (int) album year.
    :return album_type: (str) album_type.
    """
    # album text structure: "<albumtype>: <albumtitle> (<year>)"
    try:
        title = re.search('\"(.*)\"', album_text).group(1)
        year = int(re.search('\(([1-2][0-9][0-9][0-9])\)', album_text).group(1))
        album_type = album_text.split(':')[0]
    except AttributeError:
        print('Could not parse album text: {}'.format(album_text))
        title = album_text.replace(':', '')
        year = None
        album_type = None

    return title, year, album_type


def load_artist_discography(artist_lyrics_url, chromedriver_path,
                            headless=True):
    """
    Browse the artist's lyrics website, iterate over all albums and songs
    and save the links to each song's lyrics webpage.
    :param artist_lyrics_url: (str) link to the azlyrics artist webpage.
    :param chromedriver_path: (str) path to the chromedriver executable.
    :param headless: (boolean) if set as False the browser window will be shown,
        otherwise, it will not.
    :return parsed_songs: {str->Song object} dictionary in which the keys are
        song titles and the values are the corresponding Song objects, with the
        attributes 'title', 'track_number', 'album' and 'instrumental' set.
    :return parsed_albums: {str->Album object} dictionary in which the keys are
        album titles and the values are the corresponding Album objects, with
        the attributes 'title', 'year', 'number' and 'album_type' set.
    """
    # Enter site:
    options = Options()
    if headless:
        options.add_argument("--headless")  # to not see browser window
    driver = webdriver.Chrome(chromedriver_path, options=options)
    driver.get(artist_lyrics_url)
    print('{}\tEntered \"{}\" site successfully'
          .format(datetime.now(), driver.title))

    # Reach list of all albums and songs from website:
    albums_and_songs_parent = \
        driver.find_element_by_xpath("//div[@id='listAlbum']")
    albums_and_songs_list = \
        albums_and_songs_parent.find_elements_by_tag_name('div')

    # Iterate over list and save albums and songs information:
    parsed_albums, parsed_songs = {}, {}
    album_number = 1

    for el in albums_and_songs_list:

        el_type = el.get_attribute("class")
        el_text = el.text.rstrip()

        if el_type == 'album':  # album
            album_title, year, album_type = parse_album_text(el_text)
            album = Album(album_title)
            album.year = year
            album.number = album_number
            album.album_type = album_type
            parsed_albums[album.title] = album
            album_number += 1
            current_track_number = 1

        elif el_type == 'listalbum-item':  # song
            song_title, instrumental = parse_song_text(el_text)
            # when a song appears more than once in the discography, modify
            # the "parsed_songs" dictionary key for this song to include all:
            if song_title in parsed_songs:
                song_key = song_title + ' ({})'.format(album.title)
            else:
                song_key = song_title

            song = Song(song_title)

            song.track_number = current_track_number
            song.album = album
            song.instrumental = instrumental

            if not song.instrumental:
                song.lyrics_url = \
                    el.find_element_by_tag_name('a').get_attribute('href')
            parsed_songs[song_key] = song
            current_track_number += 1

    driver.close()

    return parsed_songs, parsed_albums
