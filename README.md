# SoundScraping
Scraping SoundCloud and Beatport to build the world's largest and most comprehensive dataset on the features, popularity, artworks and audience reactions to techno tracks.

## Why scrape SoundCloud and Beatport?
In the age of views, followers and charts, the most popular music is advantaged in our personalised recommendation systems. But does popularity mean quality? Isn't music, and especially electronic music, meant to directly make us feel certain emotions?

SoundCloud comments are linked to particular moments in a track. SoundCloud also provides popularity metrics (likes, reposts, plays). Beatport provides accurate audio features. This scraper enables the collection of multimodal information about all the tracks and DJ sets that your favourite artists have posted in SoundCloud.

## Scraping artists' profiles from SoundCloud
The _SearchTracks_ class searches for the SoundCloud profile of given artists, stores descriptive information, accesses each track's page, and scrapes each track's popularity metrics and all comments. Specifically, it collects:

1. Artist followers
2. Artist bio
3. Artist location
4. Profile and background images
5. Each track's likes, reposts, and plays
6. Track images
7. All comments and their timings

## Getting accurate audio features and metadata from Beatport
The _TrackInfo_ class searches for each track scraped from SoundCloud on Bearport. If the sound was a track and not a DJ set, it scrapes:

1. BPM
2. Key
3. Genre
4. Release date
5. Producers, remixers
6. Waveform image

## Storing data
The scraper currently stores data in local .csv files

## Next steps
Building on this first iteration, I plan to:

1. Improving the pipeline for searching artists by using SoundCloud searches rather than URL queries
2. Scraping more artists, more tracks, more comments with more time and perhaps parallel scripting
3. Transfering everything to the cloud and using an SQL database
4. Conduct sentiment analysis on comments and extract audio features from mp3 track files
5. Use ML predict sentiment and popularity from audio features
6. Generate track images and sounds that can be tuned to desired sentiments

