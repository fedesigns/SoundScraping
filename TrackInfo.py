import Scraper
import SearchTracks
import pandas as pd


class TrackInfo():

    '''
    This class includes methods to retrieve the information of a particular track: comments, artist information, likes, shares
    '''
    
    def __init__(self, track_url):
    
        self.scraper = Scraper()
        self.artist_name = artist_name
        self.track_url = track_url
        self.open_track = scraper.driver.get(url_string)

        sleep(1)  #leave time to load


    def open_track(self):
        current_items = scraper.driver.find_elements_by_xpath('') # need this?
    
    
    def get_track_info(self):
        artist_name = 
        artist_bio = 
        artist_location = 
        artist_followers

