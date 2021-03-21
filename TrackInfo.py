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
                self.result_artists = self.scrape.driver.find_element_by_xpath(f'//*[@id="pjax-inner-wrapper"]/section/main/div/div[4]/ul/li[{r+1}]/div[2]/p[2]/a[1]').text
                ## checking if there is a second artist
                try:
                    self.result_artist_2 = self.scrape.driver.find_element_by_xpath(f'//*[@id="pjax-inner-wrapper"]/section/main/div/div[4]/ul/li[{r+1}]/div[2]/p[2]/a[2]').text
                    self.result_artists = self.result_artists + ", " + self.result_artist_2
                    self.result_remixer = self.scrape.driver.find_element_by_xpath(f'//*[@id="pjax-inner-wrapper"]/section/main/div/div[4]/ul/li[{r+1}]/div[2]/p[3]/a').text
                    result_artists_all = self.result_artists + ", " + self.result_remixer

                except:
                    print('only one artist')

                ### Checking if the names of track and artist match our soundcloud data
                if lower(result_name) in lower(self.track_name)
                or lower(self.track_name) in lower(result_name) 
                and lower(self.artist_name) in lower(result_artists_all):
                    print('Track found!')
                    track_found = True
                    self.track_url = self.scrape.driver.find_element_by_xpath(f'//*[@id="pjax-inner-wrapper"]/section/main/div/div[4]/ul/li[{r+1}]/div[2]/p[1]/a').get_attribute('href')
                    break

        except:
            track_found = False
            print('Could not find track')

        if track_found == True:
            
            # creating dict to store scraped data
            self.beat_dict = {
                                'BPM': None,
                                'Key': None,
                                'Genre': None,
                                'Waveform': None,
                                'Length': None,
                                'Type': None,
                                'Mix': None,
                                'Feat': None,
                                'Remixer': None,
                                'OriginalProducer': None
                                }

            ## opening track page
            self.scraper.driver.get(self.track_url)
            sleep(2)

            ## getting information 
            try: 
                bpm = self.scraper.driver.find_element_by_xpath('//*[@id="pjax-inner-wrapper"]/section/main/div[2]/div/ul[2]/li[3]/span[2]').text
                self.beat_dict['BPM'] = bpm
                print('BPM: ', bpm)
            except:
                print('No bpm')

            try: 
                key = self.scraper.driver.find_element_by_xpath('//*[@id="pjax-inner-wrapper"]/section/main/div[2]/div/ul[2]/li[4]/span[2]').text
                self.beat_dict['Key'] = key
                print('Key: ', key)
            except:
                print('No key')

            try: 
                genre = self.scraper.driver.find_element_by_xpath('//*[@id="pjax-inner-wrapper"]/section/main/div[2]/div/ul[2]/li[5]/span[2]/a').text
                self.beat_dict['Genre'] = genre
                print('Genre: ', genre)
            except:
                print('No genre')   

            try: 
                waveform = self.scraper.driver.find_element_by_xpath('//*[@id="react-track-waveform"]').get_attribute("data-src")
                self.beat_dict['Waveform'] = waveform
                print('Waveform: ', waveform)
            except:
                print('No Waveform')           

            try: 
                length = self.scraper.driver.find_element_by_xpath('//*[@id="pjax-inner-wrapper"]/section/main/div[2]/div/ul[2]/li[1]/span[2]').text
                self.beat_dict['Length'] = length
                print('Length: ', length)
            except:
                print('No Length')  
            
            self.beat_dict['Type'] = "Track"

            try:
                mix = self.scraper.driver.find_element_by_xpath('                //*[@id="pjax-inner-wrapper"]/section/main/div[1]/div[1]/h1[2]').text
                self.beat_dict['Length'] = length
                print('Length: ', length)
                //*[@id="pjax-inner-wrapper"]/section/main/div[1]/div[1]/h1[2]
            except:
                print('No mix information')
            
            try:
                self.beat_dict['Feat'] = self.result_artist_2
            except:
                print('No feat')

            try:
                self.beat_dict['Remixer'] = self.result_remixer
            except:
                print('No remixer')

            try:
                self.beat_dict['OriginalProducer'] = self.result_artists
        
            except:
                print('Did not find artists')
            
        