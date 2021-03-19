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

## reading dataframes: artists from my Spotify, comments from soundcloud, track information
artists_df = pd.read_csv('Artists.csv')
comments_df = pd.read_csv('Comments.csv', index_col=False)
tracks_df = pd.read_csv('Tracks.csv', index_col=False)

print(artists_df.head())
#print(comments_df.head())
#print(tracks_df.head())
## accessing files to store scraped data
#%%

## scraping the soundcloud page for each artist
### move driver calls here to avoid quitting and restarting each time?

for i in range(artists_df['ArtistName'].count()):

    artist = artists_df.iloc[i, 0]
    print(artist)

    searcher = SearchTracks.SearchTracks(artist)

    searcher.scrape_page()

    searcher.get_artist_info()

    keys = list(searcher.artist_info.keys())
    print(keys)
    ## adding scraped data to our Artist dataframe
    for k in range(len(keys)):
        print(keys[k])
        artists_df[keys[k]][i] = searcher.artist_info[keys[k]]

    searcher.scraper.driver.quit()

    print(artists_df.head())



### create temporary dfs inside functions/loop and append those to main ones?
### handling NaN? nee to add them manually?



# %%
