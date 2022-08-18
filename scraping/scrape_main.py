from datetime import datetime
from scraping.scrape_discography_azlyrics import load_artist_discography
from scraping.scrape_lyrics_azlyrics import scrape_lyrics_songs_azlyrics
from scraping.find_artist_url import find_artist_url
from songs_and_albums.songs_and_albums import write_songs_json
import configparser
from configparser import NoOptionError
from os.path import join
from common.common import string_for_path


def lyrics_scraping_main(artist, chromedriver_path, output_path, headless=True,
                         specific_songs=None):
    """
    Given the name of an artist, this function performs the following tasks:
    1) Calls "find_artist_url" function, which introduces the provided artist
       name in the Az-lyrics website search and returns the URL to the webpage
       that contains the discography of the first artist in the search results.
    2) Calls "load_artist_discography" function, which goes to the previously
       found URL with the artist discography and extracts general information
       of each album and song. For each non-instrumental song, the URL to its
       lyrics' webpage is saved too.
    3) Calls "scrape_lyrics_songs_azlyrics" function, which loads the lyrics'
       webpage of each song, and saves the lyrics and songwriters of each song
       to their corresponding Song object attribute.
    4) Calls "write_songs" function, which writes the obtained information of
       all songs to an output file.
    :param artist: (str) name of the artist
    :param chromedriver_path: (str) path to the chromedriver executable file.
    :param output_path: (str) path to which the output file will be created.
    :param headless: (boolean) if set as False the browser window will be shown,
        otherwise, it will not.
    :param specific_songs: ([str]) if a list of song titles is provided, only
        the lyrics of the songs by the artist with titles contained in this
        list will be scraped.
    """
    # Load the artist's discography azlyrics webpage
    artist, artist_discography_url = find_artist_url(artist, chromedriver_path,
                                                     headless=headless)

    # Load all the songs and albums, and the URLs to the song lyrics,
    # from artist webpage in azlyrics:
    songs, albums = load_artist_discography(artist_discography_url,
                                            chromedriver_path,
                                            headless=headless)
    print('{}\tFound {} albums and {} songs.'
          .format(datetime.now(), len(albums), len(songs)))

    # Add artist as song attribute
    for song in songs.values():
        song.artist = artist

    # in case only specific songs are required, filter these:
    if specific_songs is not None:
        low_specific_songs = set([s.lower() for s in specific_songs])
        songs = \
            {k: v for k, v in songs.items() if k.lower() in low_specific_songs}

    # Iterate over songs and access their lyrics URLs to scrape their lyrics:
    scrape_lyrics_songs_azlyrics(songs, chromedriver_path, headless=headless)
    print('{}\tLyrics scraping finished successfully.'.format(datetime.now()))

    # Write results in output file:
    write_songs_json(songs, output_path)
    print('{}\tAll lyrics written to output file.'.format(datetime.now()))


if __name__ == '__main__':
    # LAUNCH THIS SCRIPT TO PROVIDE ARGUMENTS WITH CONFIGURATION FILE

    # Initialise config parser:
    config_file_path = r"C:\Users\pablo\ProjectsData\Lyrics\configuration_files\Bowie_discography.cfg"
    parser = configparser.ConfigParser()
    parser.read(config_file_path)

    # Load parameters from configuration file:
    artist = parser.get("config", "artist")
    chromedriver_path = parser.get("config", "chromedriver_path")
    output_dir = parser.get("config", "output_dir")
    headless = not parser.getboolean("config", "show_window")
    try:
        specific_songs = set(parser.get("config", "songs").split(','))
    except NoOptionError:
        specific_songs = None

    # Build output path:
    output_path = join(output_dir,
                       '{}_lyrics.json'.format(string_for_path(artist)))

    # Launch scraping process:
    lyrics_scraping_main(artist, chromedriver_path, output_path,
                         headless=headless, specific_songs=specific_songs)
