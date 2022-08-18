from common.songs_and_albums import load_songs_json
from wordclouds.plot_wordcloud import plot_and_save_wordcloud
from common.common import string_for_path, create_subdir
from common.clean_lyrics import apply_lowercase, filter_pos
from os.path import dirname, join
from wordcloud import WordCloud
from datetime import datetime


def get_word_cloud(lyrics, title, output_dir, min_word_length=0,
                   stopwords=set(), pos_tags=set()):
    """
    Generates a wordcloud of some given lyrics under some specifications.
    :param lyrics: (str)
    :param title: (str) title of the word cloud chart.
    :param output_dir: (str) directory under which the output word cloud will
        be created.
    :param min_word_length: (int) discard words shorter than N characters.
    :param stopwords: ([str])
    :param pos_tags: ([str])
    """
    # clean lyrics
    lyrics = apply_lowercase(lyrics)

    # keep only words of a certain part-of-speech (e.g. nouns, verbs...)
    if pos_tags:
        lyrics = filter_pos(lyrics, pos_tags)

    try:
        # generate word cloud from lyrics:
        word_cloud = WordCloud(width=450, height=450, max_font_size=100,
                               random_state=8,
                               min_word_length=min_word_length,
                               stopwords=stopwords).generate(lyrics)
        # write word cloud to a file:
        file_name = string_for_path(title)
        output_path = join(output_dir, file_name)
        plot_and_save_wordcloud(word_cloud, title, output_path)
    except ValueError:
        # no lyrics (instrumental, or all stopwords)
        pass


def word_clouds_main(input_path, stopwords_path=None):
    """
    Generate files with word clouds of all songs and albums in the provided
    input file.
    :param input_path: (str) path to the input file with the songs information.
    :param stopwords_path: (str) path to the input file with the stopwords.
    """
    # generate base output directory from input path:
    base_output_dir = create_subdir(dirname(input_path), 'wordclouds')

    # load songs and albums information from input file:
    songs, albums = load_songs_json(input_path)

    # stopwords to consider when specified so:
    if stopwords_path is None:
        stopwords_path = 'stopwords.txt'
    stopwords = set([line.rstrip() for line in open(stopwords_path)])

    # albums:
    albums_dir = create_subdir(base_output_dir, 'albums')
    for album in albums.values():
        album_lyrics = ' '.join([song.lyrics for song in album.songs
                                 if song.lyrics is not None])
        chart_title = '({}) {}'.format(album.year, album.title)
        get_word_cloud(album_lyrics,
                       chart_title,
                       albums_dir)
        get_word_cloud(album_lyrics,
                       chart_title + '\n*removing stopwords*',
                       albums_dir,
                       stopwords=stopwords)
        get_word_cloud(album_lyrics,
                       chart_title + '\n*only nouns*',
                       albums_dir,
                       stopwords=stopwords,
                       pos_tags={'NN', 'NNS', 'NNP', 'NNPS'})
    print('{}\tAlbum word clouds written.'.format(datetime.now()))

    # songs:
    songs_dir = create_subdir(base_output_dir, 'songs')
    for song in songs.values():
        if song.instrumental:
            continue
        chart_title = '({}: {})\n{} - {}'.format(song.album.year,
                                                 song.album.title,
                                                 song.track_number,
                                                 song.title)
        get_word_cloud(song.lyrics,
                       chart_title,
                       songs_dir)
        get_word_cloud(song.lyrics,
                       chart_title + '\n*removing stopwords*',
                       songs_dir,
                       stopwords=stopwords)
        get_word_cloud(song.lyrics,
                       chart_title + '\n*only nouns*',
                       songs_dir,
                       stopwords=stopwords,
                       pos_tags={'NN', 'NNS', 'NNP', 'NNPS'})
    print('{}\tSong word clouds written.'.format(datetime.now()))

    # songwriters
    songwriter_to_lyrics = {}
    for song in songs.values():
        if song.instrumental:
            continue
        for sw in song.songwriters:
            if sw not in songwriter_to_lyrics:
                songwriter_to_lyrics[sw] = ''
            songwriter_to_lyrics[sw] += '{}\n\n'.format(song.lyrics)

    songwriters_dir = create_subdir(base_output_dir, 'songwriters')
    for songwriter, sw_lyrics in songwriter_to_lyrics.items():
        chart_title = 'Songwriter: {}'.format(songwriter)
        get_word_cloud(sw_lyrics,
                       chart_title,
                       songwriters_dir)
        get_word_cloud(sw_lyrics,
                       chart_title + '\n*removing stopwords*',
                       songwriters_dir,
                       stopwords=stopwords)
        get_word_cloud(sw_lyrics,
                       chart_title + '\n*only nouns*',
                       songwriters_dir,
                       stopwords=stopwords,
                       pos_tags={'NN', 'NNS', 'NNP', 'NNPS'})
    print('{}\tSongwriter word clouds written.'.format(datetime.now()))

    print('{}\tAll word clouds written.'.format(datetime.now()))


if __name__ == '__main__':
    i_path = r"C:\Users\pablo\ProjectsData\Lyrics\david_bowie_lyrics.csv"
    word_clouds_main(i_path)
