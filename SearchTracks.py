import Scraper
import pandas as pd
from time import sleep


class SearchTracks():
    '''
    This class launches the search for all tracks of a given artist or label on SoundCloud.
    '''
    
    def __init__(self, tracks_df, comments_df):
        '''
        Initialises the class
        '''
        self.tracks_df = tracks_df
        self.comments_df = comments_df
        
        # Dictionaries storing the data we ultimately want to scrape
        self.artist_info = {'Bio': None, 'Location': None, 'Followers': None, 'ProfileImageURL': None, 'BackgroundImageURL': None} #'ArtistName': None,  declaring dictionary to store info


        ### can all of these run inside init function or should they be a separate method?
        
    def scrape_page(self, artist_input):
        '''
         launches a scraper that gets all items from the web page of a given artist
        '''  
        self.artist_name = artist_input
        artist_words = self.artist_name.split()

        # trying the first of two possibilities for how artist names are entered in the URL: no spaces between words
        self.artist_string_no_space = "".join(artist_words)
        self.artist_string_dashes = "-".join(artist_words)
        self.artist_url_no_space = f"https://www.soundcloud.com/{self.artist_string_no_space}/tracks" #need to handle exceptions as some artists have paths firstnamelastname and some have firstname-lastname
        self.artist_url_dashes = f"https://www.soundcloud.com/{self.artist_string_dashes}/tracks"
 
        # getting all elements in the page, trying dashes format first
        self.scraper = Scraper.Scraper()
        self.artist_items = self.scraper.driver.get(self.artist_url_dashes)

        try:
            ## checking if it's not an error page
            sleep(1)
            self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div/div[2]/h3')
            
            ## checking if we didn't land on a fake profile
            followers_string_test = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div[2]/div/article[1]/table/tbody/tr/td[1]/a').get_attribute('title')
            print(followers_string_test[0])
            followers_strings_test = followers_string_test.split()
             
            if len(followers_strings_test[0]) < 4:
                self.artist_items = self.scraper.driver.get(self.artist_url_no_space)
            
            print('here at try')

        except:
            ### need to fix issue here - check on ben klock
            sleep(1)
            self.artist_items = self.scraper.driver.get(self.artist_url_no_space)
            
            if len(followers_strings_test[0]) < 4:
                self.artist_items = self.scraper.driver.get(self.artist_url_no_space)
            
            print(self.artist_url_no_space)
            print(self.artist_items)
            print('looking for tracks')
            sleep(2)
            #self.artist_items = self.scraper.driver.get(self.artist_url_dashes)

        # self.items = # store all selenium web elements here? or extract later?
        # except:
          #  print("There was an error searching for {f}'s page".format(artist_name))

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
        self.scraper.scroll(0, 100000)
        sleep(1)
        self.scraper.scroll(0, 100000)
        sleep(1)
        self.scraper.scroll(0, 100000)
        sleep(1)
        self.scraper.scroll(0, 100000)
        sleep(1)
        #print('here')


        ### ADD if/Else FOR THE TWO TYPES OF ARTIST NAME ENTRIES INTO URL STRING
        ### CHECK USE OF SELF. WHEN DECLARING LOCAL VARIABLES. need to declare all in init fn?
    
    def get_artist_info(self):  ### need to add artist_items in input and add self. to variables?
        '''
        Extracts information about the artist and stores it in a dictionary
        '''
        
        #name = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div/div[2]/h3').text()
        #self.artist_info['ArtistName'] = name
        #print('Name', name)

        try:
            bio = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div[2]/div/article[1]/div[1]/div/div/div/div/p').text
            self.artist_info['Bio'] = bio
            print('Bio', bio)
        except:
            print('No bio found')

        #collecting the information in the header and subheader. can contain location, artist name, 'pro unlimited'
        try:
            subheader = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div/div[2]/h4[2]').text
            header = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div/div[2]/h4[1]').text
            self.artist_info['Location'] = header + "" + subheader
            print(location, 'Location')
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
        self.artist_info['Followers'] = int(followers)
        print(followers, 'Followers')

        # getting a string containing image metadata, splitting it at '"', to save the url in the dict
        try:
            profile_image_string = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div/div[1]/div/span').get_attribute('style')
            profile_image_strings = profile_image_string.split('"')
            profile_image_url = profile_image_strings[1]
            self.artist_info['ProfileImageURL'] = profile_image_url
            print(profile_image_url, 'Profile Image URL')
        except:
            print('no profile image')
        # getting a string containing background image metadata, splitting it at '(',')' to obtain its url
        try:
            background_image_string = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[2]/div').get_attribute('style')
            background_image_strings = background_image_string.split('")')
            background_image_url = background_image_strings[0].split('("')[1]  ### will this work in one line?
            self.artist_info['BackgroundImageURL'] = background_image_url
            print(background_image_url, 'BackgroundImageURL')
        except:
            print('no background image')
        # need return?
        

    def get_artist_tracks(self):   
        '''
        This function extracts all items in the HTML tree that contain 'soundList' information, 
        then iterates through all elements in an artist's page that contain track titles and URLs, 
        extracts  features, and stores them in lists in a dictionary
        
        For each track, we access the page and scrape its information and comments
        '''
        ### NOT WORKING - double check paths
        ### switch to loop iterating through xpaths like zoopla example
        #track_items = self.scraper.driver.find_elements_by_class_name("soundList__item")
        
        track_items = '//ul/[@class="soundList__item"]/li'
        # self.scraper.driver.find_elements_by_xpath('//*[@id="content"]/div/div[4]/div[1]/div/div[2]/div/ul/[@class="soundList__item"')
        # could also use find_element_by_class_name()
        print('got {} track items!'.format(len(track_items)))
        # print(len(track_items))

       
        for t in range(len(track_items)): ### FIX THIS LOOP. separate search for tracks and scraping of each track, or just go back to search page each time
            
            # sleep(1)

            ## if not the first iteration, go back to track page before opening next one
            if t > 0:
                self.scraper.driver.execute_script("window.history.go(-1)")
                sleep(3)
                self.scraper.scroll(0, 100000)
                sleep(1)
                self.scraper.scroll(0, 100000)
                sleep(1)
                self.scraper.scroll(0, 100000)
                sleep(1)
                self.scraper.scroll(0, 100000)
                sleep(1)

            if t >= 100:
                break


            # print(f'track {t+1}')
            #title_element = track_items[i].find_element_by_class_name("soundTitle__title sc-link-dark")  ### index using get() instead? may have to find_element_by_xpath() and update li[] index within xpath at each loop iteration
            
            title_element = self.scraper.driver.find_element_by_xpath(f'//*[@id="content"]/div/div[4]/div[1]/div/div[2]/div/ul/li[{t+1}]/div/div/div[2]/div[1]/div/div/div[2]/a')

            #//*[@id="content"]/div/div[4]/div[1]/div/div[2]/div/ul/li[34]/div/div/div[2]/div[1]/div/div/div[2]/a

            # print(f'got title element {t+1}')
            track_href = title_element.get_attribute('href')
            track_url = track_href # need to concatenate domain and href? eg "https://www.soundcloud.com" + 
            track_name = title_element.find_element_by_tag_name('span').text
        
            ##for t in range(len(track_items)):

            # storing the data in the track's dict
            ### REFORMAT TO REMOVE NONEs when beatport works
            self.track_dict = {
                                'TrackName': [], 
                                'TrackURL': [], 
                                'ArtistName': [self.artist_name],
                                'TrackDescription': [],
                                'Likes': [],
                                'CommentsCount': [],
                                'Shares': [],
                                'Plays': [],
                                'TrackImageURL': [],
                                'TrackDate': [],
                                'Tags': [None],
                                'BPM': [None],
                                'Key': [None],
                                'Genre': [None],
                                'Waveform': [None],
                                'Length': [None],
                                'Type': [None],
                                'Mix': [None],
                                'Feat': [None],
                                'Remixer': [None],
                                'OriginalProducer': [None]
                                }

            # adding track name to temporary dict
            self.track_dict['TrackName'].append(track_name)  # add track ids?
            print('TrackName: ', track_name)
            
            # adding track URL
            self.track_dict['TrackURL'].append(track_url)
            print('TrackURL: ', track_url)

            ## opening track page
            self.scraper.driver.get(track_url)
            sleep(1)
            
            ## finding track description. 
            try: 
                description_element = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div/div[1]/div/p[1]')
                track_description = description_element.text
                self.track_dict['TrackDescription'].append(track_description)
                print('Track description: ', track_description)
            except:
                print('No track description')
                self.track_dict['TrackDescription'].append(None)


            ## finding likes. 
            try:
                likes_element = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li[2]')
                likes_string = likes_element.get_attribute('title')
                likes_strings = likes_string.split()
                likes_digits = likes_strings[0].split(',')
                likes = "".join(likes_digits)
                self.track_dict['Likes'].append(int(likes))
                print('Track likes: ', likes)
            except:
                print('No likes found')
                self.track_dict['Likes'].append(None)
               

            ## finding shares. 
            try:
                shares_element = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li[3]/a/span[2]')
                shares_string = shares_element.text
                shares_strings = shares_string.split()
                shares_digits = shares_strings[0].split(',')
                shares = "".join(shares_digits)
                self.track_dict['Shares'].append(int(shares))
                print('Shares: ', shares)
            except:
                print('No shares found')
                self.track_dict['Shares'].append(None)


            ## finding plays. 
            try: 
                plays_el = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li[1]/span/span[1]')
                plays_string = plays_el.text
                plays_strings = plays_string.split()
                plays_digits = plays_strings[0].split(',')
                plays = "".join(plays_digits)                
                self.track_dict['Plays'].append(int(plays))
                print('Plays: ', plays)
            except:
                print('No plays found')
                self.track_dict['Plays'].append(None)


            ## finding the URL of the track's image. 
            try:
                image_el = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[2]/div[1]/div/div/div/span') ### need to add splitting code
                image_string = image_el.get_attribute('style')
                image_strings = image_string.split('")')
                track_image_url = image_strings[0].split('("')[1]  ### will this work in one line?
                self.track_dict['TrackImageURL'].append(track_image_url)
                print(track_image_url)
            except:
                print('No image found')
                self.track_dict['TrackImageURL'].append(None)

            ## finding the date of release (posting). 
            try:
                release_date_el = self.scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[2]/div[3]/div/time')
                release_datetime = release_date_el.get_attribute('datetime')
                self.track_dict['TrackDate'].append(release_datetime)
                print(release_datetime)
            except:
                print('No release date found')
                self.track_dict['TrackDate'].append(None)

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
            
            ## getting comments
            #try: 
            comment_items = self.scraper.driver.find_elements_by_class_name("commentsList__item")
            # may have to use e.g.: 
            # comment_items = '//ul/[@class="commentsList__item"]/li'  ### do we need to go one level up?
            # self.scraper.driver.find_elements_by_xpath('//*[@id="content"]/div/div[4]/div[1]/div/div[2]/div/ul/[@class="soundList__item"')
            # could also use find_element_by_class_name()
            print('got {} comments!'.format(len(comment_items)))
            self.track_dict['CommentsCount'].append(len(comment_items))
    
            for c in range(len(comment_items)):
                
                ### GET CORRECT PATH
                # define comment element here or go straight to sub elements below?        

                # creating a dictionary to store information about each particular comment
                self.comment_dict = {
                                'Comment': [], 
                                'CommentDateTime': [], 
                                'TrackTime': [],
                                'TrackName': [track_name],
                                'TrackURL': [track_url]
                                }

                ### FILL WITH PATHS

                ## finding comment text
                try: 
                    comment_el = self.scraper.driver.find_element_by_xpath(f'//*[@id="content"]/div/div[3]/div[1]/div/div[2]/div[2]/div/div[3]/ul/li[{c+1}]/div/div/div[1]/div/span/p')
                    comment = comment_el.text 
                    self.comment_dict['Comment'].append(comment)
                    #print('Comment: ', comment)

                except:
                    print('No comment text found')
                    self.comment_dict['Comment'].append(None)


                ## finding comment date and time
                try: 
                    datetime_el = self.scraper.driver.find_element_by_xpath(f'//*[@id="content"]/div/div[3]/div[1]/div/div[2]/div[2]/div/div[3]/ul/li[{c+1}]/div/div/div[2]/span/time')
                    comment_datetime = datetime_el.get_attribute("datetime")
                    self.comment_dict['CommentDateTime'].append(comment_datetime)
                    #print('Posted on: ', comment_datetime)
                except:
                    print('No comment text found')
                    self.comment_dict['CommentDateTime'].append(None)


                ## finding the time of the track that the comment was posted at
                try:
                    track_time_el = self.scraper.driver.find_element_by_xpath(f'//*[@id="content"]/div/div[3]/div[1]/div/div[2]/div[2]/div/div[3]/ul/li[{c+1}]/div/div/div[1]/span/span/a')
                    track_time = track_time_el.text
                    self.comment_dict['TrackTime'].append(track_time)
                    #print('At track time: ', track_time)
                except:
                    print('No tracktime found')
                    self.comment_dict['TrackTime'].append(None)

                
                ### ERROR BELOW HERE? 

                ## creating df from comments dict and appending it to original comments df
                temp_comments_df = pd.DataFrame.from_dict(self.comment_dict)
                self.comments_df = self.comments_df.append(temp_comments_df, ignore_index=True)
                print(self.comments_df)

            ## trying to infer whether the music is a set or a track by looking at its last comment.
            ## soundcloud hides the duration element somehow as part of the waveform graphic.
            ## so we look at the lask comment in the track's timeline.
            ## If it's more that 15' into the track, we assume the sound to be a set.
            ## We will only search for tracks, not sets, on Beatport

            '''
            Try sorting this, alternatively check type on beatport
            ### need to convert time string to e.g. datetime or seconds to find max?
            track_comments_df = comments_df[comments_df['TrackName']==track_name]
            split_tracktime['TrackTime'] = track_comments_df['TrackTime'].apply(lambda x: x.split(':'))
            seconds_tracktime['Seconds'] = split_tracktime['TrackTime'].apply(lambda x: 3600 * int(x[0]) + 60 * int(x[1]) + int(x[2]) if len(x) == 3)
            seconds_tracktime['Seconds'] = split_tracktime['TrackTime'].apply(lambda x: 60 * int(x[0]) + int(x[1]) if len(x) == 2)
            seconds_tracktime['Seconds'] = split_tracktime['TrackTime'].apply(lambda x: int(x[0]) if len(x) == 1)

            last_comment_time = max(comments_df[comments_df['TrackName']==track_name]
            print(last_comment_time)
            if last_comment_time < 900:
                print('this is a track, need to search it on beatport')
                ## search for track in beatport
            '''
            
            # use new dict, append to df every time like for tracks
            temp_track_df = pd.DataFrame(self.track_dict)
            self.tracks_df = self.tracks_df.append(temp_track_df, ignore_index=True)

            print(self.tracks_df)
                


                ### CONVERT COMMENT DICT TO DF, APPEND TO MAIN COMMENT DF

            #except:
            #    print('No comments found')

            #going back to artist page - NEEDED?
            ## driver.execute_script("window.history.go(-1)")

            ### GO TO BEATPORT HERE

            ### CONVERT TRACK_DICT TO DF AND APPEND TO MAIN DF

        # track_urls = scraper.driver.find_elements_by_xpath('//*[@id="content"]/div/div[4]/div[1]/div/div[2]/div/ul/li[1]/div/div/div[2]/div[1]/div/div/div[2]/a')   # find element or elements?
        return self.tracks_df, self.comments_df

