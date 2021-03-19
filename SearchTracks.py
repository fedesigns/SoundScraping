import Scraper
import pandas as pd


class SearchTracks(artist_name):
    '''
    This class launches the search for all tracks of a given artist or label on SoundCloud.
    '''
    
    def __init__(self, artist_name):
        '''
        Initialises the class, launches a scraper that gets all items from the web page of a given artist
        '''
        self.scraper = Scraper()
        self.artist_name = artist_name
        self.artist_url = f"https://www.soundcloud.com/{artist_name}/tracks" #need to handle exceptions as some artists have paths firstnamelastname and some have firstname-lastname
        self.artist_ = scraper.driver.get(url_string)
        # self.items = # store all selenium web elements here? or extract later?

        sleep(1)  #leave time to load, then scroll down a few times to load all tracks
        scraper.scroll(0, 100000)
        sleep(1)
        scraper.scroll(0, 100000)
        sleep(1)
        scraper.scroll(0, 100000)

    
    def get_artist_info(self):
        '''
        Extracts information about the artist
        '''
        
        # getting a string containing 'XXX,XXX followers' and cleaning it to save an integer in the dict
        followers_string = scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div[2]/div/article[1]/table/tbody/tr/td[1]/a').get_attribute('title')
        followers_strings = followers_string.split()
        followers = ''
        if len(followers_strings[0]) > 3:
            followers_string = followers_strings[0].split(',')
            for s in followers_string:    ### need to use range()?
                followers += followers_string[s]
            followers = int(followers)
        else: 
            followers = int(followers_strings[0])

        artist_info['followers'].append(followers)

        profile_image_url = scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div/div[1]/div/span')
        profile

        cover_image_url = 


    def get_tracks(self, track_items):    # take track as input?
        '''
        This function extracts all items in the HTML tree that contain 'soundList' information, 
        then iterates through all elements in an artist's page that contain track titles and URLs, 
        extracts these two features, and stores them in lists in a dictionary
        '''

        track_items = scraper.driver.find_elements_by_xpath('//*[@id="content"]/div/div[4]/div[1]/div/div[2]/div/ul/[@class="soundList__item"')
        # could also use find_element_by_class_name()

        artist_tracks = {'track_name': [], 'track_url': []}
        for i in track_items:
            title_element = track_items[i].find_element_by_class_name("soundTitle__title sc-link-dark").
            track_href = title_element.get_attribute('href')
            track_url = "https://www.soundcloud.com" + track_href # concatenating domain and href
            track_name = title_element.find_element_by_tag_name('span').text
            artist_tracks['track_name'].append(track_name)  # add track ids?
            artist_tracks['track_url'].append(track_url)

        # track_urls = scraper.driver.find_elements_by_xpath('//*[@id="content"]/div/div[4]/div[1]/div/div[2]/div/ul/li[1]/div/div/div[2]/div[1]/div/div/div[2]/a')   # find element or elements?


