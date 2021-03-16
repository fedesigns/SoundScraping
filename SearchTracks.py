import Scraper
import pandas as pd


class SearchTracks():

    '''
    This class launches the search for all tracks of a given artist or label on SoundCloud.
    Results have filtered to have length between 2 and 10 minutes and are tagged #techno
    '''
    
    def __init__(self, artist_name):
    
        self.scraper = Scraper()
        self.artist_name = artist_name
        self.artist_url = f"https://www.soundcloud.com/{artist_name}/tracks"
        self.open_artist_page = scraper.driver.get(url_string)

        sleep(1)  #leave time to load


    def open_track(self):
        current_items = scraper.driver.find_elements_by_xpath('') # need this?

    
    def get_artist_info(self):
        artist_name = 
        artist_bio = 
        artist_location = 
        artist_followers

