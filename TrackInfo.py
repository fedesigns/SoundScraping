import Scraper
import pandas as pd
from time import sleep
from CloudSaving import s3_save_image, update_row

class TrackInfo():

    '''
    This class includes methods to scrape Beatport to find more information about the tracks scraped from soundcloud
    '''
    
    def __init__(self, tracks_df):
        '''
        initialises the class, takes the tracks df as attribute
        '''
        self.tracks_df = tracks_df
        
    
    def beatport_scraper(self, trackID, artistID, track_input, artist_input, s3_client, hostname):
        '''
        searches Beatport for a given track
        '''
        
        self.track_name = track_input
        self.artist_name = artist_input
        self.search_content = track_input + " " + artist_input

        ## creating the string that will be used to request track in Beatport via URL
        search_words = self.search_content.split()
        search_string = "+".join(search_words)

        search_url = "https://www.beatport.com/search?q=" + search_string
        print(search_url)
        

        self.scrape = Scraper.Scraper()
        self.result_items =  self.scrape.driver.get(search_url)
        sleep(10)
        track_found = False
        
        #closing pop up
        try:
            pop_up_el = self.scrape.driver.find_element_by_class_name('bx-close-link')
            self.scrape.driver.execute_script("arguments[0].click();", pop_up_el)
            sleep(2)
        except:
            print('Pop up did not show up')

        ## iterating through search results
        for r in range(6):
            ## selecting search result
            self.result_name = self.scrape.driver.find_element_by_xpath(f'//*[@id="pjax-inner-wrapper"]/section/main/div/div[4]/ul/li[{r+1}]/div[2]/p[1]/a/span[1]').text
            self.result_artists = self.scrape.driver.find_element_by_xpath(f'//*[@id="pjax-inner-wrapper"]/section/main/div/div[4]/ul/li[{r+1}]/div[2]/p[2]/a[1]').text
            result_artists_all = self.result_artists
            ## checking if there is a second artist
            try:
                self.result_artist_2 = self.scrape.driver.find_element_by_xpath(f'//*[@id="pjax-inner-wrapper"]/section/main/div/div[4]/ul/li[{r+1}]/div[2]/p[2]/a[2]').text
                result_artists_all = self.result_artists + ", " + self.result_artist_2
            except:
                print('only one artist')
            
            try:
                self.result_remixer = self.scrape.driver.find_element_by_xpath(f'//*[@id="pjax-inner-wrapper"]/section/main/div/div[4]/ul/li[{r+1}]/div[2]/p[3]/a').text
                result_artists_all = result_artists_all + ", " + self.result_remixer 
                
            except:
                print('No remixer')
            
            ### Checking if the names of track and artist match our soundcloud data
            if self.artist_name.lower() in result_artists_all.lower() and (self.result_name.lower() in self.track_name.lower() or self.track_name.lower() in self.result_name.lower()):
                print('Track found!')
                track_found = True
                self.track_url = self.scrape.driver.find_element_by_xpath(f'//*[@id="pjax-inner-wrapper"]/section/main/div/div[4]/ul/li[{r+1}]/div[2]/p[1]/a').get_attribute('href')
                break
        
        if track_found == False:
            self.tracks_df.loc[self.tracks_df['track_name']==self.track_name,'is_track'] = False

        if track_found == True:
            
            # creating dict to store scraped data
            self.beat_dict = {
                                'bpm': None,
                                'key': None,
                                'genre': None,
                                'waveform_url': None,
                                'waveform_path': None,
                                'length': None,
                                'is_track': None,
                                'mix': None,
                                'feat': None,
                                'remixer': None,
                                'original_producer': None,
                                'beatport_url': self.track_url,
                                'beatport_track_name': self.result_name,
                                'label': None,
                                'beatport_release': None
                                }

            ## opening track page
            self.scrape.driver.get(self.track_url)
            sleep(2)


            ## getting information 
            try: 
                bpm = self.scrape.driver.find_element_by_xpath('//*[@id="pjax-inner-wrapper"]/section/main/div[2]/div/ul[2]/li[3]/span[2]').text
                self.beat_dict['bpm'] = int(bpm)
                # print('BPM: ', bpm)
            except:
                print('No bpm')

            try: 
                key = self.scrape.driver.find_element_by_xpath('//*[@id="pjax-inner-wrapper"]/section/main/div[2]/div/ul[2]/li[4]/span[2]').text
                self.beat_dict['key'] = key
                # print('Key: ', key)
            except:
                print('No key')

            try: 
                genre = self.scrape.driver.find_element_by_xpath('//*[@id="pjax-inner-wrapper"]/section/main/div[2]/div/ul[2]/li[5]/span[2]/a').text
                self.beat_dict['genre'] = genre
                # print('Genre: ', genre)
            except:
                print('No genre')   

            try: 
                waveform_url = self.scrape.driver.find_element_by_xpath('//*[@id="react-track-waveform"]').get_attribute("data-src")
                self.beat_dict['waveform_url'] = waveform_url
                # print('Waveform: ', waveform)
                waveform_path = s3_save_image(waveform_url, artistID, trackID, self.artist_name, self.track_name, 'waveforms', s3_client, 'sound-scraping')
                self.beat_dict['waveform_path'] = waveform_path
            except:
                print('No Waveform')           

            try: 
                length_text = self.scrape.driver.find_element_by_xpath('//*[@id="pjax-inner-wrapper"]/section/main/div[2]/div/ul[2]/li[1]/span[2]').text
                length_strings = length_text.split(":")
                if len(length_strings) == 2:
                    length = int(length_strings[0]) * 60 + int(length_strings[1]) 
                elif len(length_strings) == 3:
                    length = int(length_strings[0]) * 3600 + int(length_strings[1]) * 60 + int(length_strings[2]) 
            
                self.beat_dict['length'] = length
                # print('Length: ', length)
            except:
                print('No Length')  
            
            self.beat_dict['IsTrack'] = True

            try:
                mix = self.scrape.driver.find_element_by_xpath('//*[@id="pjax-inner-wrapper"]/section/main/div[1]/div[1]/h1[2]').text
                self.beat_dict['mix'] = mix
                # print('Mix: ', mix)
            except:
                print('No mix information')
            
            try:
                self.beat_dict['feat'] = self.result_artist_2
            except:
                print('No feat')

            try:
                remixers = self.scrape.driver.find_element_by_xpath('//*[@id="pjax-inner-wrapper"]/section/main/div[2]/div/div[2]/span[2]/a').text
                self.beat_dict['remixer'] = remixers

            except:
                print('No remixer')

            try:
                self.beat_dict['original_producer'] = self.result_artists
        
            except:
                print('Did not find artists')

            try:
                label = self.scrape.driver.find_element_by_xpath('//*[@id="pjax-inner-wrapper"]/section/main/div[2]/div/ul[2]/li[6]/span[2]/a').text
                self.beat_dict['label'] = label
                # print('Label: ', label)
            except:
                print('No label found')

            try:
                release = self.scrape.driver.find_element_by_xpath('//*[@id="pjax-inner-wrapper"]/section/main/div[2]/div/ul[2]/li[2]/span[2]').text
                self.beat_dict['beatport_release'] = release
                # print('Released on ', release)
            except:
                print('No release date found')  

            # inserting scraped data into Tracks df
            '''
            self.tracks_df.loc[self.tracks_df['TrackName']==self.track_name,'BPM'] = int(bpm)
            self.tracks_df.loc[self.tracks_df['TrackName']==self.track_name,'Waveform'] = self.beat_dict['Waveform']
            self.tracks_df.loc[self.tracks_df['TrackName']==self.track_name,'Key'] = self.beat_dict['Key']
            self.tracks_df.loc[self.tracks_df['TrackName']==self.track_name,'Length'] = self.beat_dict['Length']
            self.tracks_df.loc[self.tracks_df['TrackName']==self.track_name,'Genre'] = self.beat_dict['Genre']
            self.tracks_df.loc[self.tracks_df['TrackName']==self.track_name,'Type'] = self.beat_dict['Type']
            self.tracks_df.loc[self.tracks_df['TrackName']==self.track_name,'Mix'] = self.beat_dict['Mix']
            self.tracks_df.loc[self.tracks_df['TrackName']==self.track_name,'Feat'] = self.beat_dict['Feat']
            self.tracks_df.loc[self.tracks_df['TrackName']==self.track_name,'Remixer'] = self.beat_dict['Remixer']
            self.tracks_df.loc[self.tracks_df['TrackName']==self.track_name,'OriginalProducer'] = self.beat_dict['OriginalProducer']
            self.tracks_df.loc[self.tracks_df['TrackName']==self.track_name,'BeatportURL'] = self.beat_dict['BeatportURL']
            self.tracks_df.loc[self.tracks_df['TrackName']==self.track_name,'BeatportTrackName'] = self.beat_dict['BeatportTrackName']
            self.tracks_df.loc[self.tracks_df['TrackName']==self.track_name,'Label'] = self.beat_dict['Label']
            self.tracks_df.loc[self.tracks_df['TrackName']==self.track_name,'BeatportRelease'] = self.beat_dict['BeatportRelease']
            '''

            # updating tracks_df for local storage and RDS table
            cols = list(self.beat_dict.keys())
            for k in range(len(cols)):
                self.tracks_df.loc[self.tracks_df['track_name']==self.track_name, cols[k]] = self.beat_dict[cols[k]]
                
                col = cols[k]
                val = str(self.beat_dict[cols[k]])
                update_row('tracks_and_beats', col, val, 'track_id', trackID, hostname)
                sleep(0.5)

            # updating row in RDS table
            
            ## Adding new row to RDS track
            # # print(self.tracks_df)
            # values_tracks = f"{self.track_dict['track_id'][0]}, {self.track_dict['artist_id'][0]}, '{self.track_dict['track_name'][0]}', '{self.track_dict['track_url'][0]}', " + \
            #     f"'{self.track_dict['artist_name'][0]}', '{self.track_dict['track_description'][0]}', {self.track_dict['likes'][0]}, {self.track_dict['comments_count'][0]}, " + \
            #     f"{self.track_dict['shares'][0]}, {self.track_dict['plays'][0]}, '{self.track_dict['track_image_url'][0]}', '{self.track_dict['track_image_path'][0]}', " + \
            #     f"'{self.track_dict['track_date_time'][0]}', '{self.track_dict['tags'][0]}'"
            # print(values_artists)
            # track_columns = "track_id, artist_id, track_name, track_url, artist_name, track_description, likes, comments, shares, plays, track_image_url, track_image_path, track_date_time, tags"            

           
            

            return self.tracks_df