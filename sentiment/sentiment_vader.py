from nltk.sentiment.vader import SentimentIntensityAnalyzer
from process_lyrics.clean_lyrics import apply_lowercase


def get_songs_sentiments_vader(songs):
    """
    Obtain the sentiment scores (positive, negative and compound values) of the
    lyrics of a set of songs and add these values to the corresponding
    attributes of the song objects.
    :param songs: {str->Song object} dictionary in which the keys are song
        titles and the values are the corresponding Song objects.
    """
    # Initialise sentiment analyzer:
    sia = SentimentIntensityAnalyzer()

    # for each song:
    for song in songs.values():

        # load lyrics:
        lyrics = song.lyrics

        # clean lyrics:
        lyrics = apply_lowercase(lyrics)
        while '  ' in lyrics:
            lyrics = lyrics.replace('  ', ' ')

        # skip instrumental songs
        if not lyrics:
            song.positive_sentiment = 0.
            song.negative_sentiment = 0.
            song.compound_sentiment = 0.
            continue

        # get positivity, negativity and compound scores for songs with lyrics:
        scores = sia.polarity_scores(lyrics)
        song.positive_sentiment = scores['pos']
        song.negative_sentiment = scores['neg']
        song.compound_sentiment = scores['compound']
