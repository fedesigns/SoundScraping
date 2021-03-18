import Scraper
import SearchTracks
import TrackInfo
import pandas as pd

artists = pd.read_csv('Artists.csv')

'''
need to do some pre processing to programmatically format artists' names as suitable for URL strings
'''
for artist in artists['Artist']:

    searcher = SearchTracks(artist)

    # need to scroll down until all tracks load. Add conditional to control this better e.g. based on changes in length of page
    searcher.scraper.scroll(0, 100000)

