import Scraper
import pandas as pd


class SearchTracks():
    '''
    This class launches the search for all tracks of a given artist or label on SoundCloud.
    '''
    
    def __init__(self, artist_name):
        '''
        Initialises the class
        '''
        self.scraper = Scraper()
        self.artist_name = artist_name
        
        # Dictionaries storing the data we ultimately want to scrape
        self.artist_info = {'name': [], 'bio': [], 'location': [], 'followers': [], 'profile_image_url': [], 'background_image_url': []} # declaring dictionary to store info
        self.artist_tracks = {'track_name': [], 'track_url': []}


        ### can all of these run inside init function or should they be a separate method?
        
    def scrape_page(self):
        '''
         launches a scraper that gets all items from the web page of a given artist
        '''  
        artist_words = self.artist_name.split()

        ### need to extend this try/except to the whole script when automating - in loop using this class for different artists
        # trying the first of two possibilities for how artist names are entered in the URL: no spaces between words
        artist_string_no_space = "".join(artist_words)
        artist_string_dashes = "-".join(artist_words)
        self.artist_url_no_space = f"https://www.soundcloud.com/{artist_string_no_space}/tracks" #need to handle exceptions as some artists have paths firstnamelastname and some have firstname-lastname
        self.artist_url_dashes = f"https://www.soundcloud.com/{artist_string}/tracks"
 
        # getting all elements in the page, trying nospace format first
        self.artist_items = scraper.driver.get(artist_url_no_space)

        try:
            if scraper.driver.find_element_by_class_name("errorTitle").text == "We can't find that user."
                self.artist_items = scraper.driver.get(artist_url_dashes)
            else:
                continue
        except:
            continue

        # self.items = # store all selenium web elements here? or extract later?


        sleep(1)  #leave time to load, then scroll down a few times to load all tracks
        scraper.scroll(0, 100000)  ### reduce distance? will it give errors if too far?
        sleep(1)
        scraper.scroll(0, 100000)
        sleep(1)
        scraper.scroll(0, 100000)
        sleep(1)



        ### ADD if/Else FOR THE TWO TYPES OF ARTIST NAME ENTRIES INTO URL STRING
        ### CHECK USE OF SELF. WHEN DECLARING LOCAL VARIABLES. need to declare all in init fn?
    
    def get_artist_info(self):  ### need to add artist_items in input and add self. to variables?
        '''
        Extracts information about the artist and stores it in a dictionary
        '''
        
        name = scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div/div[2]/h3'.text
        self.artist_info['name'].append(name)
        
        bio = scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div[2]/div/article[1]/div[1]/div/div/div/div/p').text
        self.artist_info['bio'].append(bio)

        location = scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div/div[2]/h4[1]').text
        self.artist_info['location'].append(location)

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
        self.artist_info['followers'].append(followers)

        # getting a string containing image metadata, splitting it at '"', to save the url in the dict
        profile_image_string = scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div/div[1]/div/span').get_attribute('style')
        profile_image_strings = profile_image_string.split('"')
        profile_image_url = profile_image_strings[1]
        self.artist_info['profile_image_url'].append(profile_image_url)

        # getting a string containing background image metadata, splitting it at '(',')' to obtain its url
        background_image_string = scraper.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[2]/div').get_attribute('style')
        background_image_strings = background_image_string.split(')')
        background_image_url = background_image_strings[0].split('(')[1]  ### will this work in one line?
        self.artist_info['background_image_url'].append(background_image_url)

        # need return?
        

    def get_artist_tracks(self):   
        '''
        This function extracts all items in the HTML tree that contain 'soundList' information, 
        then iterates through all elements in an artist's page that contain track titles and URLs, 
        extracts these two features, and stores them in lists in a dictionary
        '''

        track_items = scraper.driver.find_elements_by_xpath('//*[@id="content"]/div/div[4]/div[1]/div/div[2]/div/ul/[@class="soundList__item"')
        # could also use find_element_by_class_name()
        
        for i in track_items:
            title_element = track_items[i].find_element_by_class_name("soundTitle__title sc-link-dark")  ### index using get() instead? may have to find_element_by_xpath() and update li[] index within xpath at each loop iteration
            track_href = title_element.get_attribute('href')
            track_url = "https://www.soundcloud.com" + track_href # concatenating domain and href
            track_name = title_element.find_element_by_tag_name('span').text
            
            self.artist_tracks['track_name'].append(track_name)  # add track ids?
            self.artist_tracks['track_url'].append(track_url)

        # track_urls = scraper.driver.find_elements_by_xpath('//*[@id="content"]/div/div[4]/div[1]/div/div[2]/div/ul/li[1]/div/div/div[2]/div[1]/div/div/div[2]/a')   # find element or elements?


