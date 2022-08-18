from scraping.scrape_main import lyrics_scraping_main
from common.common import string_for_path


def concatenate_files(input_paths, output_path):
    """
    Reads a list of files and concatenates their lines to an output file.
    :param input_paths: ([str]) list of paths to input files.
    :param output_path: (str) path to output concatenated file.
    """
    first_header = True
    with open(output_path, 'w') as output_file:
        for i_path in input_paths:
            header = True
            for line in open(i_path):
                if header and not first_header:
                    pass
                else:
                    output_file.write(line)
                header = False
                first_header = False


if __name__ == '__main__':
    ch_path = r'C:\Users\pablo\PycharmProjects\chromedriver.exe'
    output_path = r"C:\Users\pablo\ProjectsData\Lyrics\Various\concat.csv"
    songs_path = r""
    songs = [line.rstrip().split('|') for line in open(songs_path)]

    out_paths = []

    for artist, song in songs:
        out_path = \
            r"C:\Users\pablo\ProjectsData\Lyrics\Various\{}_{}_lyrics.csv"\
            .format(string_for_path(artist), string_for_path(song))
        try:
            lyrics_scraping_main(artist, ch_path, out_path, headless=True,
                                 specific_songs=[song])
            out_paths.append(out_path)
        except BaseException as e:
            print(artist, '-', song, e)

    concatenate_files(out_paths, output_path)
