import Scraper
import SearchTracks
import pandas as pd


class TrackInfo():

    '''
    This class includes methods to scrape Beatport to find more information about the tracks scraped from soundcloud
    '''
    
    def __init__(self, tracks_df):
        '''
        initialises the class, takes the tracks df as attribute
        '''
        self.tracks_df = tracks_df
        
    
    def beatport_scraper(self, track_input, artist_input):
        '''
        searches Beatport for a given track
        '''
        
        self.track_name = track_input
        self.artist_name = artist_input
        search_content = track_input + " " + artist_input

        ## creating the string that will be used to request track in Beatport via URL
        search_words = self.search_content.split()
        search_string = "+".join(search_words)
        try:
            search_url = "https://www.beatport.com/q=" + track_string
            self.scrape = Scraper.Scraper()
            self.result_items =  self.scrape.driver.get(self.artist_url_dashes)
            sleep(2)
            
            ## iterating through search results
            for r in range(6):
                ## selecting search result
                result_name = self.scrape.driver.find_element_by_xpath(f'//*[@id="pjax-inner-wrapper"]/section/main/div/div[4]/ul/li[{r+1}]/div[2]/p[1]/a/span[1]').text
                result_artists = self.scrape.driver.find_element_by_xpath(f'//*[@id="pjax-inner-wrapper"]/section/main/div/div[4]/ul/li[{r+1}]/div[2]/p[2]/a[1]').text
                ## checking if there is a second artist
                try:
                    result_artist_2 = self.scrape.driver.find_element_by_xpath(f'//*[@id="pjax-inner-wrapper"]/section/main/div/div[4]/ul/li[{r+1}]/div[2]/p[2]/a[2]').text
                    result_artists = result_artists + ", " + result_artist_2
                    result_remixer = self.scrape.driver.find_element_by_xpath(f'//*[@id="pjax-inner-wrapper"]/section/main/div/div[4]/ul/li[{r+1}]/div[2]/p[3]/a').text
                    result_artists = result_artists + ", " + result_remixer

                except:
                    print('only one artist')

                ### Checking if the names of track and artist match our soundcloud data
                if lower(result_name) in lower(self.track_name)
                or lower(self.track_name) in lower(result_name) 
                and lower(self.artist_name) in lower(result_artists):
                    print('Track found!')
                    track_found = True
                    self.track_url = self.scrape.driver.find_element_by_xpath(f'//*[@id="pjax-inner-wrapper"]/section/main/div/div[4]/ul/li[{r+1}]/div[2]/p[1]/a').get_attribute('href')
                    break

        except:
            track_found = False
            print('Could not find track')

        if track_found == True:
            
        
    
    def get_track_info(self):
        artist_name = 
        artist_bio = 
        artist_location = 
        artist_followers
        

        ### need a lot of scrolling to load all comments

        ### include replies in same comment? or separate object?
