from common.songs_and_albums import load_songs_json, \
    write_songs_json, write_songs_csv
from sentiment.sentiment_vader import get_songs_sentiments_vader
from sentiment.plot_sentiments import plot_albums_avg_sentiments
from os.path import dirname, join
from common.common import create_subdir


def songs_sentiments_main(input_path):
    """
    Performs sentiment analysis of a series of songs.
    :param input_path: (str) path to the input file with the song lyrics.
    """
    # load songs and albums information from input file:
    songs, albums = load_songs_json(input_path)

    # get the positive, negative and compound sentiments of son lyrics with
    # VADER method:
    get_songs_sentiments_vader(songs)

    # write the VADER song sentiments to a CSV file:
    base_output_dir = create_subdir(dirname(input_path), 'sentiments')
    output_path = join(base_output_dir, 'vader_lyrics_sentiments.json')
    write_songs_json(songs, output_path)
    output_path = join(base_output_dir, 'vader_lyrics_sentiments.csv')
    write_songs_csv(songs, output_path)

    # write a scatter plot with average positive-negative VADER sentiments
    # of each album:
    output_plot_path = join(base_output_dir, 'vader_album_lyrics_sentiments')
    plot_albums_avg_sentiments(albums, output_plot_path)


if __name__ == '__main__':
    songs_path = r"C:\Users\pablo\ProjectsData\Lyrics\David Bowie\sentiments\vader_lyrics_sentiments.json"
    songs_sentiments_main(songs_path)
