'''
This script calls our scraper functions to obtain:

1. A list of all the soundcloud tracks on given artists, and their URLs
2. Information about the artist (profile image, bio, followers, location, name)

Then, we will go to the soundcloud URL of each track to scrape:
1. all comments and their metadata
2. popularity metrics (likes, shares)
3. the track's artwork

Finally, we will find the page for each track on Beatport to scrape:
1. its BPM
2. its key
3. its genre tags

Further work will include:
1. Moving everything to the cloud
2. downloading relevant tracks as mp3 files using soundcouldtomp3.com, storing them in a data lake
3. conducting signal processing on audio files to extract additional features to analyse
4. automating the selection of artists to expand the dataset by searching for record labels in souncloud or by using the Spotify API 
'''
#%%
import Scraper
import SearchTracks
# import TrackInfo
import pandas as pd
from datetime import datetime


## reading dataframes: artists from my Spotify, comments from soundcloud, track information
artists_df = pd.read_csv('Artists.csv')
comments_df = pd.read_csv('Comments.csv')#, index_col=False)
tracks_df = pd.read_csv('Tracks.csv')#, index_col=False)

print(artists_df.head())
#print(comments_df.head())
#print(tracks_df.head())
## accessing files to store scraped data
#%%

## scraping the soundcloud page for each artist
### move driver calls here to avoid quitting and restarting each time?
#try:
searcher = SearchTracks.SearchTracks(tracks_df, comments_df)

for i in range(artists_df['ArtistName'].count()):

    artist = artists_df.iloc[i, 0]
    print(artist)

    searcher.scrape_page(artist)

    ## getting artist information
    searcher.get_artist_info()
    keys = list(searcher.artist_info.keys())
    # print(keys)
    ## adding scraped data to our Artist dataframe
    for k in range(len(keys)):
        # print(keys[k])
        artists_df[keys[k]][i] = searcher.artist_info[keys[k]]


    ## getting track names and URLs
    searcher.get_artist_tracks()
    
    #track_list = searcher.artist_tracks['TrackName']
    #track_url_list = 

    #for j in range(len(track_list)):
    #    tracks_df['TrackName'][j] = track_list[j]

    # creating a temporary df with this artist's tracks
    #temp_df = pd.DataFrame(searcher.artist_tracks)
    ## appending temporary dataframe to the main tracks df
    #tracks_df = tracks_df.append(temp_df, ignore_index=True)

    print(tracks_df)
    # searcher.scraper.driver.quit()
    # print(artists_df.head())

now = datetime.now()
print(artists_df)
print(searcher.comments_df)
print(searcher.tracks_df)

artists_df.to_csv('Artists-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)
searcher.comments_df.to_csv('Comments-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)
searcher.tracks_df.to_csv('Tracks-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)


#saving scraped data if error occurs
#except:
#    now = datetime.now()
 #   artists_df.to_csv('Artists-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)
  #  comments_df.to_csv('Comments-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)
   # tracks_df.to_csv('Tracks-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)


### create temporary dfs inside functions/loop and append those to main ones?
### handling NaN? nee to add them manually?



# %%
# %%
