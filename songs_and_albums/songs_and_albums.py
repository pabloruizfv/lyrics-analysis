from process_lyrics.words import get_num_words, get_num_unique_words
import csv
import json
from copy import deepcopy


class Song:
    def __init__(self, title):
        self.title = title
        self.artist = None
        self.track_number = None
        self.album = Album('unknown')
        self.lyrics_url = None
        self.lyrics = None
        self.instrumental = None
        self.songwriters = set()
        self.positive_sentiment = None
        self.negative_sentiment = None
        self.compound_sentiment = None


class Album:
    def __init__(self, title):
        self.title = title
        self.year = None
        self.number = None
        self.album_type = None
        self.songs = []

    def sort_songs(self):
        # sort the album songs attribute by track number:
        song_name_to_obj = {song.title: song for song in self.songs}
        self.songs = [song_name_to_obj[num_song_tuple[1]] for num_song_tuple in
                      sorted(self.tracklist().items(), key=lambda x: x[0])]

    def lyrics_list(self):
        # list in which each element contains a string with lyrics from a song:
        self.sort_songs()
        return [song.lyrics for song in self.songs]

    def joined_lyrics(self, delimiter=' '):
        # string with lyrics of all album songs, joined by space by default:
        return delimiter.join(self.lyrics_list())

    def tracklist(self):
        # dictionary relating each track number with the song title:
        return {song.track_number: song.title for song in self.songs}

    def song_title(self, track_number):
        # Obtain the title of the song given the track number:
        return self.tracklist()[track_number]

    def song_titles(self):
        # List with song titles sorted by track number:
        self.sort_songs()
        return [t[1] for t in self.tracklist().items()]

    def songwriters(self):
        # set with all songwriters appearing in at least one song of the album:
        return set().union(*[song.songwriters for song in self.songs])

    def songwriters_count(self):
        # dictionary relating each songwriter to the number of written songs:
        songwriters_dict = {}
        for song in self.songs:
            for sw in song.songwriters:
                if sw not in songwriters_dict:
                    songwriters_dict[sw] = 0
                songwriters_dict[sw] += 1
        return songwriters_dict


def write_songs_json(songs, output_path):
    """
    Write a set of songs' information in a JSON output file.
    :param songs: {str->Song object} dictionary in which the keys are song
        titles and the values are the corresponding Song objects to write.
    :param output_path: (str): path to which the output file will be written.
    """
    with open(output_path, 'w', encoding="utf-8") as output_file:
        for song in deepcopy(songs).values():
            song.album.songs = []
            song.album = vars(song.album)
            song.songwriters = list(song.songwriters)
            song_dict = vars(song)
            song_dict['num_words'] = get_num_words(song.lyrics)
            song_dict['num_unique_words'] = get_num_unique_words(song.lyrics)
            output_file.write('{}\n'.format(json.dumps(song_dict)))


def load_songs_json(input_path):
    """
    Load Song and Album objects and as many of their attributes as possible
    from the information written in a JSON input file.
    :param input_path: (str) path to the input CSV file containing the songs'
        information.
    :return songs: {str->Song object} dictionary in which the keys are song
        titles and the values are the corresponding Song objects.
    :return albums: {str->Album object} dictionary in which the keys are album
        titles and the values are the corresponding Album objects.
    """
    songs, albums = {}, {}

    for line in open(input_path, 'r', encoding="utf-8"):

        # Load JSON dictionary:
        json_dict = json.loads(line.rstrip())

        # SONG:
        # Initialise song:
        song = Song(json_dict['title'])
        # Add all song attributes:
        for key, value in json_dict.items():
            setattr(song, key, value)
        # Songwriters attribute appears as a list in JSON file, turn to set:
        song.songwriters = set(song.songwriters)
        # Create song key and add to songs dictionary:
        song_key = '{} - {}'.format(song.title, song.album['title'])
        songs[song_key] = song

        # If the album does not exist yet, create it & add to albums dict:
        album_title = json_dict['album']['title']
        if album_title not in albums:
            album = Album(album_title)
            albums[album_title] = album
            for key, value in song.album.items():
                setattr(album, key, value)

        # Now change the album attribute of the song, which is currently a
        # dictionary, and replace it by the actual album object:
        song.album = albums[album_title]

    # Add song objects to list of songs attribute of each album:
    for song in songs.values():
        song.album.songs.append(song)

    # Sort songs list in the attribute of each album by track number:
    for album in albums.values():
        album.sort_songs()

    return songs, albums


def write_songs_csv_append(songs, output_path):
    """
    Add a set of songs' information to an existing CSV output file.
    :param songs: {str->Song object} dictionary in which the keys are song
        titles and the values are the corresponding Song objects to write.
    :param output_path: (str): path to which the output file will be written.
    """
    with open(output_path, 'a', encoding="utf-8") as output_file:
        for song in songs.values():

            lyrics = song.lyrics
            while '\n' in lyrics:
                lyrics = lyrics.replace('\n', '  ')

            output_file.write(
                '{}|{}|{}|{}|{}|{}|{}|{}|"{}"|{}|{}|{}|{}|{}\n'
                .format(song.title,
                        song.artist,
                        song.track_number,
                        song.album.title,
                        song.album.year,
                        song.album.number,
                        song.instrumental,
                        ','.join(sorted(list(song.songwriters))),
                        lyrics,
                        get_num_words(song.lyrics),
                        get_num_unique_words(song.lyrics),
                        song.positive_sentiment,
                        song.negative_sentiment,
                        song.compound_sentiment
                        )
                              )


def write_songs_csv(songs, output_path):
    """
    Write a set of songs' information in a CSV output file.
    :param songs: {str->Song object} dictionary in which the keys are song
        titles and the values are the corresponding Song objects to write.
    :param output_path: (str): path to which the output file will be written.
    """
    with open(output_path, 'w', encoding="utf-8") as output_file:
        output_file.write('title|artist|track_number|album|year|album_number|' +
                          'instrumental|songwriters|lyrics|' +
                          'words|unique_words|pos|neg|compound\n')

    write_songs_csv_append(songs, output_path)


def load_songs_csv(input_path):
    """
    Load Song and Album objects and as many of their attributes as possible
    from the information written in a CSV input file.
    :param input_path: (str) path to the input CSV file containing the songs'
        information.
    :return songs: {str->Song object} dictionary in which the keys are song
        titles and the values are the corresponding Song objects.
    :return albums: {str->Album object} dictionary in which the keys are album
        titles and the values are the corresponding Album objects.
    """
    songs, albums = {}, {}

    for line in csv.DictReader(open(input_path, encoding="utf-8"),
                               delimiter='|'):

        # initialise song:
        song = Song(line['title'])

        # initialise album if it does not exist already:
        if line['album'] not in albums:
            album = Album(line['album'])
            new_album = True
        else:
            album = albums[line['album']]
            new_album = False

        # SONG

        # add artist attribute to song:
        try:
            song.artist = line['artist']
        except KeyError:
            pass

        # add track number attribute to song:
        try:
            song.track_number = int(line['track_number'])
        except (ValueError, KeyError):
            pass

        # add album attribute to song:
        song.album = album

        # add instrumental attribute to song:
        if line['instrumental'] == 'True':
            song.instrumental = True
        elif line['instrumental'] == 'False':
            song.instrumental = False
        else:
            song.instrumental = None

        # add songwriters attribute to song:
        try:
            if line['songwriters']:
                song.songwriters = set(line['songwriters'].split(','))
        except ValueError:
            pass

        # add lyrics attribute to song:
        song.lyrics = line['lyrics']

        # add positive, negative and compound sentiment attributes to song:
        try:
            song.positive_sentiment = float(line['pos'])
        except (ValueError, KeyError):
            pass
        try:
            song.negative_sentiment = float(line['neg'])
        except (ValueError, KeyError):
            pass
        try:
            song.compound_sentiment = float(line['compound'])
        except (ValueError, KeyError):
            pass

        # add song object to dictionary:
        if line['title'] in songs:
            # if a song has the same name of an existing one, generate new key
            # for dictionary so that both songs are kept:
            key = '{} ({} {})'.format(line['title'], song.track_number,
                                      song.album.title)
        else:
            key = line['title']
        songs[key] = song

        # ALBUM

        # initialise album:
        if new_album:

            # add year attribute to album:
            try:
                album.year = int(line['year'])
            except (ValueError, KeyError):
                pass

            # add number attribute to album:
            try:
                album.number = int(line['album_number'])
            except(ValueError, KeyError):
                pass

            # add album object to dictionary:
            albums[line['album']] = album

        # add song to album songs:
        album.songs.append(song)

    # sort album songs list by track number:
    for album in albums.values():
        album.sort_songs()

    return songs, albums
