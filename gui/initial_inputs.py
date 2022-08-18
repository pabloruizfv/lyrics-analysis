from tkinter import *
from tkinter import filedialog as fd
from scraping.scrape_main import lyrics_scraping_main
from os.path import join
from common.common import string_for_path
from wordclouds.wordclouds_main import word_clouds_main
from sentiment.sentiment_main import songs_sentiments_main


def button_function(root, artist_entry, variables, headless):
    """
    Function to call when the search button is clicked. It obtains the artist
    name, the path to the chromedriver and the output directory path that have
    been manually introduced in the window boxes, and then closes the window
    and calls the "lyrics_scraping_main" function to start the lyrics web
    scraping process with these parameters.
    :param root: (Tk object) tkinter Tk root object.
    :param artist_entry: (Entry object) tkinter entry object for artist name.
    :param variables: ({str->str}) dictionary relating 'chromedriver_path' and
        'output_dir' to the corresponding specified values.
    :param headless: (boolean) if set as False the browser window will be shown,
        otherwise, it will not.
    """
    # get artist name from entry box before closing window:
    artist = artist_entry.get()
    root.destroy()

    # create output file path containing artist name (formatted):
    artist_name = string_for_path(artist).lower()
    output_path = join(variables['output_dir'], '{}_lyrics.json'
                       .format(artist_name))

    # launch lyrics web scraping process:
    lyrics_scraping_main(artist, variables['chromedriver_path'], output_path,
                         headless=headless)

    # launch word clouds generation process:
    word_clouds_main(output_path, stopwords_path='stopwords.txt')

    # launch sentiment analysis process:
    songs_sentiments_main(output_path)


def chromedriver_button_function(variables, start_button):
    """
    Function to launch when pressing chromedriver 'Select file' button.
    It just opens a window for the user to select the chromedriver file, and
    saves the path to the file under the 'chromedriver_path' key of the provided
    "variabes" dictionary.
    :param variables: ({str->str}) dictionary relating 'chromedriver_path' and
        'output_dir' to the corresponding specified values.
    :param start_button: (Button object) if all variables have been assigned
        their values, then enable the button.
    """
    variables['chromedriver_path'] = \
        fd.askopenfilename(title='Open chromedriver executable file',
                           filetypes=[('executable', 'exe')])
    if variables['chromedriver_path'] is not None and \
            variables['output_dir'] is not None:
        start_button['state'] = 'normal'


def output_button_function(variables, start_button):
    """
    Function to launch when pressing output directory 'Select directory' button.
    It just opens a window for the user to select the output directory, and
    saves the path to the directory under the 'output_dir' key of the provided
    "variabes" dictionary.
    :param variables: ({str->str}) dictionary relating 'chromedriver_path' and
        'output_dir' to the corresponding specified values.
    :param start_button: (Button object) if all variables have been assigned
        their values, then enable the button.
    """
    variables['output_dir'] = \
        fd.askdirectory(title='Select output directory')
    if variables['chromedriver_path'] is not None and \
            variables['output_dir'] is not None:
        start_button['state'] = 'normal'


def initial_inputs_gui(headless=True):
    """
    Launches a GUI consisting of a window with input boxes and a 'Start' button.
    When the 'Start' button is clicked, the values from the text boxes are
    loaded and the azlyrics web scraping process starts with the parameters
    that have been introduced.
    :param headless: (boolean) if set as False the browser window will be shown,
        otherwise, it will not.
    """
    # initialise window: title, icon, dimensions, grid
    root = Tk()
    root.title('Az-lyrics: lyrics scraper')
    icon_path = r"icon.jpg"
    root.iconbitmap(icon_path)
    root.geometry('300x300')
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # create text labels for window:
    artist_label = Label(root, text='Type in artist name:')
    chromedriver_label = Label(root, text='Chromedriver path:')
    output_label = Label(root, text='Output directory:')

    # create artist entry text box:
    artist_entry = Entry(root)

    # create variables dictionary that will be updated when pressing the
    # chromedriver and output directory buttons:
    variables = {'chromedriver_path': None, 'output_dir': None}

    # create start button, which launches all the process:
    start_button = Button(root, text='Start', state="disabled", padx=50,
                          command=lambda: button_function(root,
                                                          artist_entry,
                                                          variables,
                                                          headless))

    # create chromedriver and output directory buttons, which will launch
    # a window for the user to navigate and select the file/directory:
    chromedriver_button = \
        Button(root, text='Select file', state="normal", padx=50,
               command=lambda: chromedriver_button_function(variables,
                                                            start_button))
    output_button = \
        Button(root, text='Select directory', state="normal", padx=50,
               command=lambda: output_button_function(variables,
                                                      start_button))

    # place all the elements in their respective place in the window:
    artist_label.grid(row=0, column=0)
    artist_entry.grid(row=0, column=1)
    chromedriver_label.grid(row=1, column=0)
    chromedriver_button.grid(row=1, column=1)
    output_label.grid(row=2, column=0)
    output_button.grid(row=2, column=1)
    start_button.grid(row=3, column=0)

    root.mainloop()
