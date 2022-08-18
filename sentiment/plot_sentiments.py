import matplotlib.pyplot as plt


def get_album_avg_pos_sentiment(album):
    """
    Obtains the average positive sentiment of the songs of an album.
    :param album: (Album object)
    :return avg_pos: (float)
    """
    num_songs = len(album.songs)
    sum_pos = sum([song.positive_sentiment for song in album.songs
                  if song.positive_sentiment is not None])
    avg_pos = sum_pos / num_songs
    return avg_pos


def get_album_avg_neg_sentiment(album):
    """
    Obtains the average negative sentiment of the songs of an album.
    :param album: (Album object)
    :return avg_neg: (float)
    """
    num_songs = len(album.songs)
    sum_neg = sum([song.negative_sentiment for song in album.songs
                   if song.negative_sentiment is not None])
    avg_neg = sum_neg / num_songs
    return avg_neg


def plot_albums_avg_sentiments(albums, output_path):
    """
    Generate and write a scatter plot with the average positive and negative
    sentiment of the songs of each album.
    :param albums: {str->Album object} dictionary in which the keys are album
        titles and the values are the corresponding Album objects.
    :param output_path: {str} path to the file where the output scatter plot
        will be created.
    """
    positives, negatives, names = [], [], []

    for album in albums.values():
        pos = get_album_avg_pos_sentiment(album)
        neg = get_album_avg_neg_sentiment(album)
        positives.append(pos)
        negatives.append(neg)
        names.append(album.title)

    plt.clf()
    plt.scatter(negatives, positives)
    for i, name in enumerate(names):
        plt.annotate(name, (negatives[i], positives[i]))
    plt.title('Album Vader sentiment scores')
    plt.xlabel('negative sentiment score [0-1]')
    plt.ylabel('positive sentiment score [0-1]')
    ax = plt.gca()
    ax.set(xlim=(0, None), ylim=(0, None))
    plt.savefig(output_path)
