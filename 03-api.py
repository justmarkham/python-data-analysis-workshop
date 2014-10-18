import requests     # import module (make its functions available)

# request the data from the API
r = requests.get('http://developer.echonest.com/api/v4/artist/top_hottt?api_key=YOUR_API_KEY&format=json')
top = r.json()      # decode JSON and store in a dictionary

# pretty print for easier readability
import pprint
pprint.pprint(top)

# pull out the artist data
artists = top['response']['artists']    # list of 15 dictionaries

# reformat data into a table structure
artists_header = artists[0].keys()                      # list of 2 strings
artists_data = [artist.values() for artist in artists]  # list of 15 lists
