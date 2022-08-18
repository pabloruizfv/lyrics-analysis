from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.options import Options


def find_artist_url(artist, chromedriver_path, headless=True):
    """
    Given the name of an artist, this function loads the azlyrics main webpage,
    introduces this name in the search box and loads the results, returning
    the first artist's name and the URL to its azlyrics discography webpage.
    :param artist: (str) name of the artist
    :param chromedriver_path: (str) path to the chromedriver executable file.
    :param headless: (boolean) if set as False the browser window will be shown,
        otherwise, it will not.
    :return artist_name: (str) the actual artist name in azlyrics site.
    :return artist_discography_url: (str) URL to the artist discography webpage
        in azlyrics site.
    """
    azlyrics_url = r'https://www.azlyrics.com/'

    # Enter site:
    options = Options()
    if headless:
        options.add_argument("--headless")  # to not see browser window
    driver = webdriver.Chrome(chromedriver_path, options=options)
    driver.get(azlyrics_url)
    print('{}\tEntered \"{}\" site successfully'
          .format(datetime.now(), driver.title))

    # Find search textbox and type in artist name:
    search_textbox = driver.find_element_by_xpath(
        "//input[@class='form-control']")
    search_textbox.send_keys(artist)

    # Find search button and click:
    search_button = driver.find_element_by_xpath(
        "//button[@class='btn btn-primary']")
    search_button.click()

    # Results webpage loaded:
    results_panels = driver.find_elements_by_xpath("//div[@class='panel']")
    for panel in results_panels:
        if panel.text.startswith('Artist results:'):
            a_elements = panel.find_elements_by_tag_name("a")
            a = a_elements[0]  # first result
            artist_name = ' '.join(a.text.split(' ')[1:])
            artist_discography_url = a.get_attribute('href')
            return artist_name, artist_discography_url
