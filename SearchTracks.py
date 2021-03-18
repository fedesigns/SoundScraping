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
        scraper.scroll()

    
    def get_artist_info(self):
        '''
        Extracts information about the artist
        '''
        artist_name = 
        artist_bio = 
        artist_location = 
        artist_followers = 

    def get_track_items(self):
        '''
        Extracts all items in the HTML tree that contain 'soundList' information,
        one node per track 
        '''
        track_items = scraper.driver.find_elements_by_xpath('//*[@id="content"]/div/div[4]/div[1]/div/div[2]/div/ul/[@class="soundList__item"')
        # could also use find_element_by_class_name()

    def get_track_info(self, track_items):    # take track as input?
        '''
        This function iterates through all elements in an artist's page that contain track titles and URLs, 
        extracts these two features, and stores them in a dictionary
        '''
        for track_item in track_items:
            track_href = track_items[track].find_element_by_tag_name("a").get_attribute('href')
            track_url = "https://www.soundcloud.com" + track_href
        
        track_info = {track:'' }


        # track_urls = scraper.driver.find_elements_by_xpath('//*[@id="content"]/div/div[4]/div[1]/div/div[2]/div/ul/li[1]/div/div/div[2]/div[1]/div/div/div[2]/a')   # find element or elements?

    def get_track_name(self): # not needed if we just get names and urls from same elements?
//*[@id="content"]/div/div[4]/div[1]/div/div[2]/div/ul/li[2]

        "/html/body/div[2]/div[2]/div[2]/div/div[4]/div[1]/div/div[2]/div/ul/li[2]/div/div/div[2]/div[1]/div/div/div[2]/a/span"
        /html/body/div[2]/div[2]/div[2]/div/div[4]/div[1]/div/div[2]/div/ul/li[1]/div/div/div[2]/div[1]/div/div/div[2]/a
        /html/body/div[2]/div[2]/div[2]/div/div[4]/div[1]/div/div[2]/div/ul/li[2]/div/div/div[2]/div[1]/div/div/div[2]/a
        "//*[@id='content']/div/div[4]/div[1]/div/div[2]/div/ul/li[1]/div/div/div[2]/div[1]/div/div/div[2]/a"
        "//*[@id="content"]/div/div[4]/div[1]/div/div[2]/div/ul/li[2]/div/div/div[2]/div[1]/div/div/div[2]/a"
    