import matplotlib.pyplot as plt


def plot_and_save_wordcloud(word_cloud, chart_title, output_path):
    """
    Given a word cloud object, and a chart title and an output file, this
    function creates a plot of the word cloud, adds the corresponding chart
    title and writes a PNG file with this word cloud to an output file.
    :param word_cloud: (WordCloud object)
    :param chart_title: (str)
    :param output_path: (str) path to which the output file will be created.
    """
    # plot word cloud and remove axis ticks and labels:
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')

    # add title to word cloud chart:
    plt.title(chart_title)

    # write word cloud to output PNG file:
    plt.savefig(output_path)
