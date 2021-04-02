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
import TrackInfo
import pandas as pd
from datetime import datetime


## reading dataframes: artists from my Spotify, comments from soundcloud, track information
artists_df = pd.read_csv('Artists-Test.csv')
comments_df = pd.read_csv('Comments-Test.csv')#, index_col=False)
tracks_df = pd.read_csv('Tracks-and-Beats-Test.csv')#, index_col=False)

#%%

## scraping the soundcloud page for each artist
searcher = SearchTracks.SearchTracks(artists_df, tracks_df, comments_df)

for i in range(15, 18):  # artists_df['ArtistName'].count()):
    try:
        artist = artists_df.iloc[i, 0]
        print(artist)

        searcher.scrape_page(artist)

        ## getting artist information
        searcher.get_artist_info()

        ## getting track names and URLs
        searcher.get_artist_tracks()
        searcher.scraper.driver.quit()

    #saving scraped data if error occurs
    except:
        now = datetime.now()
        artists_df.to_csv('Artists-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)
        searcher.comments_df.to_csv('Comments-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)
        searcher.tracks_df.to_csv('Tracks-and-Beats{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)
    
now = datetime.now()
print(searcher.artists_df)
print(searcher.comments_df)
print(searcher.tracks_df)

searcher.artists_df.to_csv('Artists-Full-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)
searcher.comments_df.to_csv('Comments-Full-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)
searcher.tracks_df.to_csv('Tracks-and-Beats-Full-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)


# %%

## Scraping Beatport
scraper = TrackInfo.TrackInfo(searcher.tracks_df)

for i in range(searcher.tracks_df['TrackName'].count()):
    
    try: 
        ## selecting track and artist to input to the scraper
        track = searcher.tracks_df.iloc[i, 0]
        artist = searcher.tracks_df.iloc[i, 2]
        print(track, ' by ', artist)

        ## scraping beatport
        scraper.beatport_scraper(track, artist)
        scraper.scrape.driver.quit()

    ## if there is an error, save progress into csv in case
    except:
        now = datetime.now()
        scraper.tracks_df.to_csv('Tracks-and-Beats-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)

now = datetime.now()
print(scraper.tracks_df)
scraper.tracks_df.to_csv('Tracks-and-Beats-Full{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)


        






# %%
 range(tracks_df['TrackName'].count())
# %%
