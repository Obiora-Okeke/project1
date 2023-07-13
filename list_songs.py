import requests
import pandas as pd
import sqlalchemy as db
import pprint
from tabulate import tabulate
import os
import spotipy
# from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util

def get_artist_id(artist_name):
    search_response = requests.get(BASE_URL + 'search',
                                   headers=headers,
                                   params={'q': artist_name,
                                           'type': 'artist',
                                           'limit': 1})
    if search_response.status_code == 200:
        artists = search_response.json()['artists']['items']
        if artists:
            return artists[0]['id']
        else:
            print(f"No artist found with the name: {artist_name}")
            new_name = input("Please input an Artist name: ")
            return get_artist_id(new_name)
    else:
        print("Error occurred while searching for the artist.")
    return None


def api_call(artist_name):
    #artist_name = input('Enter artist name: ')
    artist_id = get_artist_id(artist_name)
    r = requests.get(BASE_URL + 'artists/' + artist_id + '/related-artists',
                     headers=headers)
    return r.json()


def top_songs_call(art_name):
    artist_id = get_artist_id(art_name)
    country_code = 'US'
    r = requests.get(BASE_URL + 'artists/' + artist_id + '/top-tracks',
                     headers=headers, params={'market': country_code})
    data = r.json()
    top_songs = data['tracks'][:1]  # Limit to top 3 songs
    result = []
    for song in top_songs:
        artist_name = song['artists'][0]['name']
        song_name = song['name']
        uri = song['uri']
        result.append({
            'artist': artist_name,
            'song': song_name,
            'uri': uri
        })
    return result


def json_to_dataframe(data):
    dataframe_name = pd.DataFrame.from_dict(data['artists'])
    # if 'uri' in dataframe_name:
    #     uris = dataframe_name['uri'].map(lambda x: x.get('spotify',
    #                                                                'N/A'))
    #     dataframe_name['uris'] = uris
    if 'followers' in dataframe_name:
        fol = dataframe_name['followers'].map(lambda x: x.get('total', 'N/A'))
        dataframe_name['followers'] = fol
    return dataframe_name[['name', 'uri', 'popularity',
                           'followers']].sort_values('followers',
                                                     ascending=False)


def songs_dataframe(s):
    sdf = pd.DataFrame(s)
    return sdf


def dataframe_to_database(frame):
    frame.to_sql(
        'table_name', con=engine, if_exists='replace', index=False
    )

pd.set_option('max_colwidth', None)
client_id = "ce303767105943e9b563c582c546bcdf"
client_secret = "4f77f234a135413787ba25237ed8e819"
#CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
#CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
redirect_uri = "http://example.com"
scope = "playlist-modify-public playlist-modify-private"
AUTH_URL = "https://accounts.spotify.com/api/token"
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
})

auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']
headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
BASE_URL = 'https://api.spotify.com/v1/'
'''
dat = api_call()
adf = json_to_dataframe(dat)
rel_artitst = adf['name'].tolist()
songs = pd.DataFrame()
for ar in rel_artitst[:2]:
    ar_songs = top_songs_call(ar)
    ar_songs_df = pd.DataFrame(ar_songs)
    songs = pd.concat([songs, ar_songs_df])
print(songs)
engine = db.create_engine('sqlite:///actual_data_frame.db')
dataframe_to_database(songs)
with engine.connect() as connection:
    connect = connection.execute(db.text("SELECT * FROM table_name;"))
    query_result = connect.fetchall()

    print(tabulate(pd.DataFrame(query_result),
                   ['artist', 'song', 'uri'],
                   tablefmt="grid",
                   maxcolwidths=[None, 15, 53]))
'''