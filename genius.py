from lyricsgenius import Genius
from list_songs import global_songs
import pandas as pd
from list_songs import api_call, json_to_dataframe, top_songs_call, dataframe_to_database
from make_album import create_playlist
import urllib, urllib.request
from bs4 import BeautifulSoup
import requests
import json


CLIENT_ID = 'bZm1B5vrRPoI1-vRDCt3gKkFOsWDaMqWR-xjiT7iMEBQj0bVQoI38i1mOrEGYAjm'
CLIENT_SECRET = '5ZJNhpisxNRxKKf5sk4cKEx0DfEki4S6w3HQgWsyEPg653jJosX1200FaHZy1oGlN3R1Opu6OjyKdAfuxIywPg'

access_token = 'j3UW67ujhfqQnV61rXM9hvho7V-p-NbkHubTc3L9Htv-4BL3kmSN9Wl4l2X7InVd'
BASE_URL=  "https://api.genius.com"
headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

genius = Genius(access_token)
songs = pd.DataFrame()
genius_song_ids = []
def create(artist_name = 'pop'):
    global songs
    dat = api_call(artist_name)
    adf = json_to_dataframe(dat)
    rel_artists = adf['name'].tolist()
    # songs = pd.DataFrame()
    for ar in rel_artists[:5]:
        ar_songs = top_songs_call(ar)
        ar_songs_df = pd.DataFrame(ar_songs)
        songs = pd.concat([songs, ar_songs_df])
        # dataframe_to_database(songs)
    print('songs:', songs)
    song_ids = songs['song_id'].to_list()
    print(song_ids)
    # x = create_playlist(username, playlist_name, songs)

def get_lyrics(x):
    global genius_song_ids
    URL = 'https://genius.com/Roddy-ricch-the-box-lyrics'
    page = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15'})
    soup = BeautifulSoup(page.content, "html.parser")
    text = soup.select_one('div[class^="Lyrics__Container"], .lyrics').get_text(strip=True, separator='\n')
    print(text)

    song = genius.search_song(x)
    genius_song_ids.append(song.id)
    # lyrics = song.lyrics
    # formatted_lyrics = lyrics.replace('\r', '').replace('[', '').replace(']', '').strip()
    # formatted_lyrics = f"""{formatted_lyrics}"""
    return text

def get_annotations(x):
    request = genius.referents(song_id=x, per_page=50)
    # print('requests:', request)
    annotations = [y for x in request['referents'] for y in x['annotations']]
    fragments = [y for x in request['referents'] for y in x['fragment']]
    annotation_dict = {}
    count = 0
    for annotation in annotations:
        fragment = fragments[0]
        annotation_dict[annotation['id']] = [fragment, annotation['body']]
        count +=1
    print(annotation_dict)
    return annotation_dict


    

create()

#TO CREATE ANNOTATION
# annotation = input('Create annotation: ')
#fragment: referent/ lyric portion being annotated
# genius.create_annotation(annotation, raw_annotable= '/lyrics', fragment = '')

songs['lyrics'] = songs['song'].apply(lambda x: [get_lyrics(x)])
songs['genius_id'] = genius_song_ids
songs['annotations'] = songs['genius_id'].apply(lambda x: [get_annotations(x)])
# songs['formatted_lyrics'] = songs['song'].apply(lambda x: [genius.search_song(x).lyrics])
# print(songs)



