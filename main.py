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
from Credentials import access_key_ID, secret_access_ID, username, db_endpoint, db_port, password, database
from boto3 import resource
import os
from CloudSaving import s3_save_image, create_table, TableSQL, pd_from_table, insert_row, insert_multiple_rows, update_row

hostname = db_endpoint
## reading dataframes: artists from my Spotify, comments from soundcloud, track information
artists_df = pd.read_csv('Artists-Test.csv')
comments_df = pd.read_csv('Comments-Start.csv')#, index_col=False)
tracks_df = pd.read_csv('Tracks-and-Beats-Test.csv')#, index_col=False)
        
## setting up AWS S3 client
s3_client = resource("s3", aws_access_key_id=access_key_ID, aws_secret_access_key=secret_access_ID)
s3_endpoint = 's3.eu-west-3.amazonaws.com'

## creating AWS RDS tables
tables = TableSQL(hostname, database, username, password)
create_table(tables.create_artists, hostname, 'artists')
create_table(tables.create_tracks_and_beats, hostname, 'tracks_and_beats')
create_table(tables.create_comments, hostname, 'comments')

# starting ID counters
trackID = 0
commentID = 0
artistID = 0

#%%

## scraping the soundcloud page for each artist
searcher = SearchTracks.SearchTracks(artists_df, tracks_df, comments_df, trackID, commentID)

for i in range(artists_df['artist_name'].count()):
    try:
        artist = artists_df.iloc[i, 1]
        print(artist)

        searcher.scrape_page(artist)
        artistID += 1

        ## getting artist information
        searcher.get_artist_info(s3_client, artistID, hostname)

        ## getting track names and URLs
        
        searcher.get_artist_tracks(s3_client, artistID, hostname)
        searcher.scraper.driver.quit()

    #saving scraped data if error occurs
    except:
        now = datetime.now()
        artists_df.to_csv('Artists-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)
        searcher.comments_df.to_csv('Comments-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)
        searcher.tracks_df.to_csv('Tracks-and-Beats-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)
    
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

for j in range(searcher.tracks_df['track_name'].count()):
    
     try: 
        # retrieving track data from RDS
        # rds_tracks_df = pd_from_table('tracks_and_beats')
        
        ## selecting track and artist to input to the scraper
        track = searcher.tracks_df.iloc[j, 2]
        artist = searcher.tracks_df.iloc[j, 4]
        print(track, ' by ', artist)
        trackID = searcher.tracks_df.iloc[j, 0]
        artistID = searcher.tracks_df.iloc[j, 1]



        # checking if the track is not a DJ set by looking at whether its last comment was posted more than 15 minutes into the track
        last_comment_time = int(max(searcher.comments_df[searcher.comments_df['track_name']==track]['track_time']))
        print('Last comment at:', last_comment_time)
        if last_comment_time < 900:
            print('This is a track, need to search it on beatport')

            ## scraping beatport
            scraper.beatport_scraper(trackID, artistID, track, artist, s3_client, hostname)
            scraper.scrape.driver.quit()
        
        else:
            continue

    ## if there is an error, save progress into csv in case
    except:
        now = datetime.now()
        scraper.tracks_df.to_csv('Tracks-and-Beats-{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)

now = datetime.now()
print(scraper.tracks_df)
scraper.tracks_df.to_csv('Tracks-and-Beats-Full{}.csv'.format(now.strftime("%d%m%Y-%H%M%S")), index=False)


        


# %%
comments_df#[comments_df['TrackName']==track]['TrackTime']



# %%
 range(tracks_df['TrackName'].count())
# %%
