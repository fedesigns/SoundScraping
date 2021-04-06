import Scraper
import pandas as pd
from time import sleep
from CloudSaving import s3_save_image, insert_row, insert_multiple_rows, update_row


class SearchTracks():
    '''
    This class launches the search for all tracks of a given artist or label on SoundCloud.
    '''
    
    def __init__(self, artists_df, tracks_df, comments_df, trackID, commentID):
        '''
        Initialises the class
        '''
        self.tracks_df = tracks_df
        self.comments_df = comments_df
        self.artists_df = artists_df
        self.track_id = trackID
        self.comment_id = commentID
       
        

     
    def scrape_page(self, artist_input):
        '''
         launches a scraper that gets all items from the web page of a given artist
        '''  
        self.artist_name = artist_input

        ## searching soundcloud profiles with the artist's name
        # if the name contains multiple words, replace spaces with '%20'
        self.artist_string = self.artist_name.replace(" ", "%20")
        self.search_url = f"https://www.soundcloud.com/search/people?q={self.artist_string}"

        ## getting the link to the page of the first result
        self.scraper = Scraper.Scraper()
        self.search_items = self.scraper.driver.get(self.search_url)
        sleep(3)
        self.artist_href = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div/div[3]/div/div/div/ul/li[1]/div/div/div/h2/a').get_attribute('href')
        print(self.artist_href)
        self.artist_url = f"{self.artist_href}/tracks" 
        print(self.artist_url)
 
        # getting all elements in the page
        self.artist_items = self.scraper.driver.get(self.artist_url)

        try:
            ## checking if it's not an error page
            sleep(1)
            self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div/div[2]/h3')
            
            ## checking if we didn't land on a fake profile (with less than 1000 followers)
            followers_string_test = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div[2]/div/article[1]/table/tbody/tr/td[1]/a').get_attribute('title')
            print(followers_string_test[0])
            followers_strings_test = followers_string_test.split()
            
            # if profile has less than 1000 followers, try next result up to 4 times
            if len(followers_strings_test[0]) < 4:
                
                for r in range(2,6):
                    self.artist_href = self.scraper.driver.find_element_by_xpath(f'//*[@id="content"]/div/div/div[3]/div/div/div/ul/li[{r}]/div/div/div/h2/a').get_attribute('href')
                    self.artist_url = f"{self.artist_href}/tracks" 
                    self.artist_items = self.scraper.driver.get(self.artist_url)
                    sleep(1)

                    # checking if we didn't land on a fake profile (with less than 1000 followers)
                    followers_string_test = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div[2]/div/article[1]/table/tbody/tr/td[1]/a').get_attribute('title')
                    print(followers_string_test[0])
                    followers_strings_test = followers_string_test.split()
                    if len(followers_strings_test[0]) < 4:
                        continue
                    else:
                        break
                    
                    # stopping search if we didn't find anyone with over 1000 followers
                    return None
            
            print('Found profile')

        except:
            print("Didn't find original profile")

        sleep(1)  #leave time to load, then scroll down a few times to load all tracks
        self.scraper.scroll(0, 100000)  
        sleep(1)
        # self.scraper.scroll(0, 100000)
        # sleep(1)
        # self.scraper.scroll(0, 100000)
        # sleep(1)
        # self.scraper.scroll(0, 100000)
        # sleep(1)
        # self.scraper.scroll(0, 100000)
        # sleep(1)
        # self.scraper.scroll(0, 100000)
        # sleep(1)
        # self.scraper.scroll(0, 100000)
        # sleep(1)
        # self.scraper.scroll(0, 100000)
        # sleep(1)
        # self.scraper.scroll(0, 100000)
        # sleep(1)


    def get_artist_info(self, s3_client, artistID, hostname):  
        '''
        Extracts information about the artist and stores it in a dictionary
        '''
        # Dictionary storing artist data 
        self.artist_info = {
                            'artist_id': artistID,
                            'bio': None, 
                            'location': None, 
                            'followers': None, 
                            'profile_image_url': None, 
                            'profile_image_path': None,
                            'background_image_url': None,
                            'background_image_path': None
                            } #'ArtistName': None


        ## collecting artist bio
        try:
            bio = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div[2]/div/article[1]/div[1]/div/div/div/div/p').text
            self.artist_info['bio'] = bio.replace("'", "''")
            print('bio', bio.replace("'", "''"))
        except:
            print('No bio found')

        #collecting the information in the header and subheader. can contain location, artist name, 'pro unlimited'
        try:
            subheader = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div/div[2]/h4[2]').text.replace("'", "''")
            header = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div/div[2]/h4[1]').text.replace("'", "''")
            self.artist_info['location'] = header + ", " + subheader 
            print('Location', header + ", " + subheader)
        except:
            print("no location found")

        # getting a string containing 'XXX,XXX followers' and cleaning it to save an integer in the dict
        followers_string = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div[2]/div/article[1]/table/tbody/tr/td[1]/a').get_attribute('title')
        followers_strings = followers_string.split()
        followers = ''
        if len(followers_strings[0]) > 3:
            followers_string = followers_strings[0].split(',')
            for s in followers_string:    ### need to use range()?
                followers += s
            followers = int(followers)
        else: 
            followers = int(followers_strings[0])
        self.artist_info['followers'] = int(followers)
        print(followers, 'Followers')

        # getting a string containing image metadata, splitting it at '"', to save the url in the dict
        try:
            profile_image_string = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div/div[1]/div/span').get_attribute('style')
            profile_image_strings = profile_image_string.split('"')
            profile_image_url = profile_image_strings[1]
            self.artist_info['profile_image_url'] = profile_image_url
            # print(profile_image_url, 'Profile Image URL')

            # saving image to cloud
            profile_image_path = s3_save_image(profile_image_url, artistID, '', self.artist_name, '', 'profile-images', s3_client, 'sound-scraping')
            self.artist_info['profile_image_path'] = profile_image_path
            print('Profile img path:', profile_image_path)
        except:
            print('no profile image')

        # getting a string containing background image metadata, splitting it at '(',')' to obtain its url
        try:
            background_image_string = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[2]/div').get_attribute('style')
            background_image_strings = background_image_string.split('")')
            background_image_url = background_image_strings[0].split('("')[1]
            self.artist_info['background_image_url'] = background_image_url
            # print(background_image_url, 'BackgroundImageURL')
            
            # saving to cloud
            background_image_path = s3_save_image(background_image_url, artistID, '', self.artist_name, '', 'background-images', s3_client, 'sound-scraping')
            self.artist_info['background_image_path'] = background_image_path
            print('Backg img path:', background_image_path)
        except:
            print('no background image')


        ## adding scraped data to our Artist dataframe 
        cols = list(self.artist_info.keys())
        for k in range(len(cols)):
            self.artists_df.loc[self.artists_df['artist_name']==self.artist_name, cols[k]] = self.artist_info[cols[k]]
        
        ## adding scraped data to artists table in RDS by creating a new row
        values_artists = f"{self.artist_info['artist_id']}, '{self.artist_name}', '{self.artist_info['bio']}', '{self.artist_info['location']}', {self.artist_info['followers']}, '{self.artist_info['profile_image_url']}', '{self.artist_info['profile_image_path']}', '{self.artist_info['background_image_url']}', '{self.artist_info['background_image_path']}'"
        # print(values_artists)
        artists_columns = "artist_id, artist_name, bio, location, followers, profile_image_url, profile_image_path, background_image_url, background_image_path"            

        insert_row('artists', artists_columns, values_artists, 'artist_id', hostname)


    def get_artist_tracks(self, s3_client, artistID, hostname):   
        '''
        This function extracts all items in the HTML tree that contain 'soundList' information, 
        then iterates through all elements in an artist's page that contain track titles and URLs, 
        extracts  features, and stores them in lists in a dictionary
        
        For each track, we access the page and scrape its information and comments
        '''

        track_items = self.scraper.driver.find_elements_by_class_name('soundList__item')
        print('got {} track items!'.format(len(track_items)))
       
        for t in range(3): # len(track_items)): 

             # stopping after 50 tracks of same artist
            if t >= 2:
                break
            
            ## if not the first iteration, go back to track page before opening next one
            if t > 0:
                self.scraper.driver.execute_script("window.history.go(-1)")
                sleep(3)
                # self.scraper.scroll(0, 100000)
                # sleep(1)
                # self.scraper.scroll(0, 100000)
                # sleep(1)
                # self.scraper.scroll(0, 100000)
                # sleep(1)
                # self.scraper.scroll(0, 100000)
                # sleep(1)
            
            try:
                title_element = self.scraper.driver.find_element_by_xpath(f'//*[@id="content"]/div/div[4]/div[1]/div/div[2]/div/ul/li[{t+1}]/div/div/div[2]/div[1]/div/div/div[2]/a')
                track_href = title_element.get_attribute('href')    
                track_url = track_href 
                track_name = title_element.find_element_by_tag_name('span').text
                self.track_id += 1

            except:
                continue

            # storing the data in the track's dict
            self.track_dict = {
                                'track_id': [self.track_id],
                                'artist_id': [artistID],
                                'track_name': [], 
                                'track_url': [], 
                                'artist_name': [self.artist_name],
                                'track_description': [],
                                'likes': [],
                                'comments_count': [],
                                'shares': [],
                                'plays': [],
                                'track_image_url': [],
                                'track_image_path': [],
                                'track_date_time': [],
                                'tags': [None],
                                'bpm': [None],
                                'key': [None],
                                'genre': [None],
                                'waveform': [None],
                                'length': [None],
                                'is_track': [None],
                                'mix': [None],
                                'feat': [None],
                                'remixer': [None],
                                'original_producer': [None]
                                }

            # adding track name to temporary dict
            self.track_dict['track_name'].append(track_name.replace("'", "''"))  # add track ids?
            print('TrackName: ', track_name)
            
            # adding track URL
            self.track_dict['track_url'].append(track_url)
            print('TrackURL: ', track_url)

            ## opening track page
            self.scraper.driver.get(track_url)
            sleep(1)
            
            ## finding track description. 
            try: 
                description_element = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div/div[1]/div/p[1]')
                track_description = description_element.text
                track_des = track_description.replace("'", "''")
                self.track_dict['track_description'].append(track_des)
                print('Track description: ', track_des)
            except:
                print('No track description')
                self.track_dict['track_description'].append(None)


            ## finding likes. 
            try:
                likes_element = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li[2]')
                likes_string = likes_element.get_attribute('title')
                likes_strings = likes_string.split()
                likes_digits = likes_strings[0].split(',')
                likes = "".join(likes_digits)
                self.track_dict['likes'].append(int(likes))
                print('Track likes: ', likes)
            except:
                print('No likes found')
                self.track_dict['likes'].append(None)
               

            ## finding shares. 
            try:
                shares_element = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li[3]/a/span[2]')
                shares_string = shares_element.text
                shares_strings = shares_string.split()
                shares_digits = shares_strings[0].split(',')
                shares = "".join(shares_digits)
                self.track_dict['shares'].append(int(shares))
                print('shares: ', shares)
            except:
                print('No shares found')
                self.track_dict['shares'].append(None)


            ## finding plays. 
            try: 
                plays_el = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li[1]/span/span[1]')
                plays_string = plays_el.text
                plays_strings = plays_string.split()
                plays_digits = plays_strings[0].split(',')
                plays = "".join(plays_digits)                
                self.track_dict['plays'].append(int(plays))
                print('Plays: ', plays)
            except:
                print('No plays found')
                self.track_dict['plays'].append(None)


            ## finding the URL of the track's image. 
            try:
                image_el = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[2]/div[1]/div/div/div/span') ### need to add splitting code
                image_string = image_el.get_attribute('style')
                image_strings = image_string.split('")')
                track_image_url = image_strings[0].split('("')[1]  ### will this work in one line?
                self.track_dict['track_image_url'].append(track_image_url)
                # print(track_image_url)

            except:
                print('No image found')
                self.track_dict['track_image_url'].append(None)

            try:   
                # storing in cloud, saving path
                track_image_path = s3_save_image(track_image_url, artistID, self.track_id, self.artist_name, track_name, 'track-images', s3_client, 'sound-scraping')
                self.track_dict['track_image_path'].append(track_image_path)
            except:
                print('could not store image')
                self.track_dict['TrackImagePath'].append(None)


            ## finding the date of release (posting). 
            try:
                release_date_el = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[2]/div[3]/div/time')
                release_datetime = release_date_el.get_attribute('datetime')
                self.track_dict['track_date_time'].append(release_datetime.replace("'", "''"))
                print(release_datetime)
            except:
                print('No release date found')
                self.track_dict['track_date_time'].append(None)

            ## finding soundcloud tags. #### NOT WORKING YET
            '''
            try:
                tags_els = self.scraper.driver.find_elements_by_class_name("sc-truncate sc-tagContent") ### may have to use path not element?
                tags = ", ".join([tags_els[n].text for n in range(len(tags_els))])
                self.track_dict['Tags'].append(tags)
                print(tags)
            except:
                print('No tags found')
                self.track_dict['Tags'].append(None)
            '''

            ## scraping comments data. scroll to load all comments
            sleep(1)  #leave time to load, then scroll down a few times to load all tracks
            self.scraper.scroll(0, 100000)  ### reduce distance? will it give errors if too far?
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            self.scraper.scroll(0, 100000)  ### reduce distance? will it give errors if too far?
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            self.scraper.scroll(0, 100000)  
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            self.scraper.scroll(0, 100000)
            sleep(1)
            
            ## getting comments
            comment_items = self.scraper.driver.find_elements_by_class_name("commentsList__item")
            print('got {} comments!'.format(len(comment_items)))
            self.track_dict['comments_count'].append(len(comment_items))
    
            for c in range(len(comment_items)):
                
                self.comment_id += 1

                # creating a dictionary to store information about each particular comment
                self.comment_dict = {
                                'track_id': [self.track_id],
                                'artist_id': [artistID],
                                'comment_id': [self.comment_id],
                                'comment': [], 
                                'comment_date_time': [], 
                                'track_time': [],
                                'track_name': [track_name],
                                'track_url': [track_url]
                                }

                ## finding comment text
                try: 
                    comment_el = self.scraper.driver.find_element_by_xpath(f'//*[@id="content"]/div/div[3]/div[1]/div/div[2]/div[2]/div/div[3]/ul/li[{c+1}]/div/div/div[1]/div/span/p')
                    comment = comment_el.text 
                    comm = comment.replace("'", "''")
                    self.comment_dict['comment'].append(comm)
                    #print('Comment: ', comment)

                except:
                    print('No comment text found')
                    self.comment_dict['comment'].append(None)


                ## finding comment date and time
                try: 
                    datetime_el = self.scraper.driver.find_element_by_xpath(f'//*[@id="content"]/div/div[3]/div[1]/div/div[2]/div[2]/div/div[3]/ul/li[{c+1}]/div/div/div[2]/span/time')
                    comment_datetime = datetime_el.get_attribute("datetime")
                    self.comment_dict['comment_date_time'].append(comment_datetime)
                    #print('Posted on: ', comment_datetime)
                except:
                    print('No comment text found')
                    self.comment_dict['comment_date_time'].append(None)


                ## finding the time of the track that the comment was posted at
                try:
                    track_time_el = self.scraper.driver.find_element_by_xpath(f'//*[@id="content"]/div/div[3]/div[1]/div/div[2]/div[2]/div/div[3]/ul/li[{c+1}]/div/div/div[1]/span/span/a')
                    track_time_text = track_time_el.text 

                    # converting string to seconds integer
                    track_time_strings = track_time_text.split(":")
                    if len(track_time_strings) == 2:
                        track_time = int(track_time_strings[0]) * 60 + int(track_time_strings[1]) 
                    elif len(track_time_strings) == 3:
                        track_time = int(track_time_strings[0]) * 3600 + int(track_time_strings[1]) * 60 + int(track_time_strings[2]) 

                    self.comment_dict['track_time'].append(track_time)
                    #print('At track time: ', track_time)
                    

                except:
                    print('No tracktime found')
                    self.comment_dict['track_time'].append(None)

                ## adding comment to RDS table
                columns_comment = "track_id, artist_id, comment_id, comment, comment_date_time, track_time, track_name, track_url"
                values_comment = f"{self.comment_dict['track_id'][0]}, {self.comment_dict['artist_id'][0]}, {self.comment_dict['comment_id'][0]}, '{self.comment_dict['comment'][0]}', '{self.comment_dict['comment_date_time'][0]}', {self.comment_dict['track_time'][0]}, '{self.comment_dict['track_name'][0]}', '{self.comment_dict['track_url'][0]}'"
                insert_row('comments', columns_comment, values_comment, 'comment_id', hostname)

                ## creating df from comments dict and appending it to original comments df
                temp_comments_df = pd.DataFrame.from_dict(self.comment_dict)
                self.comments_df = self.comments_df.append(temp_comments_df, ignore_index=True)
                # print(self.comments_df)

                

            ## trying to infer whether the music is a set or a track by looking at its last comment.
            ## soundcloud hides the duration element somehow as part of the waveform graphic.
            ## so we look at the lask comment in the track's timeline.
            ## If it's more that 15' into the track, we assume the sound to be a set.
            ## We will only search for tracks, not sets, on Beatport
            ### NOT WORKING YET. Beatport error handling used instead.

            '''
            Try sorting this, alternatively check type on beatport
            ### need to convert time string to e.g. datetime or seconds to find max?
            track_comments_df = comments_df[comments_df['TrackName']==track_name]
            split_tracktime['TrackTime'] = track_comments_df['TrackTime'].apply(lambda x: x.split(':'))
            seconds_tracktime['Seconds'] = split_tracktime['TrackTime'].apply(lambda x: 3600 * int(x[0]) + 60 * int(x[1]) + int(x[2]) if len(x) == 3)
            seconds_tracktime['Seconds'] = split_tracktime['TrackTime'].apply(lambda x: 60 * int(x[0]) + int(x[1]) if len(x) == 2)
            seconds_tracktime['Seconds'] = split_tracktime['TrackTime'].apply(lambda x: int(x[0]) if len(x) == 1)

            last_comment_time = max(comments_df[comments_df['TrackName']==track_name])
            print(last_comment_time)
            if last_comment_time < 900:
                print('this is a track, need to search it on beatport')
                ## search for track in beatport
            '''
            
            # use new dict, append to df every time like for tracks
            temp_track_df = pd.DataFrame(self.track_dict)
            self.tracks_df = self.tracks_df.append(temp_track_df, ignore_index=True)

            ## Adding new row to RDS track
            # print(self.tracks_df)
            values_tracks = f"{self.track_dict['track_id'][0]}, {self.track_dict['artist_id'][0]}, '{self.track_dict['track_name'][0]}', '{self.track_dict['track_url'][0]}', " + \
                f"'{self.track_dict['artist_name'][0]}', '{self.track_dict['track_description'][0]}', {self.track_dict['likes'][0]}, {self.track_dict['comments_count'][0]}, " + \
                f"{self.track_dict['shares'][0]}, {self.track_dict['plays'][0]}, '{self.track_dict['track_image_url'][0]}', '{self.track_dict['track_image_path'][0]}', " + \
                f"'{self.track_dict['track_date_time'][0]}', '{self.track_dict['tags'][0]}'"
            # print(values_artists)
            track_columns = "track_id, artist_id, track_name, track_url, artist_name, track_description, likes, comments, shares, plays, track_image_url, track_image_path, track_date_time, tags"            

            insert_row('tracks_and_beats', track_columns, values_tracks, 'track_id', hostname)
            
        return self.artists_df, self.tracks_df, self.comments_df, self.track_id, self.comment_id, artistID

### TRACK ID STOPPING AT 50 - FIX - Try with two tracks per artist, if t > 1 break limit
### COMMENTS NOT SAVING - HANDLE COLUMN OF TRACK DESCR. GIVING OUT NONE? WHY COLUMN?
### FIX REMIXER ISSUE, drop TrackDateTime column
### TEST BEATPORT UPDATE METHOD
### Add a column for time of scraping in each table