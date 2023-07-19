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
#     URL = 'https://genius.com/Roddy-ricch-the-box-lyrics'
#     page = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15'})
#     html = BeautifulSoup(page.text, "html_parser")
#     lyrics = html.find("div", class_="lyrics").get_text()
    # add = genius.search_song(x).api_path
    # querystring = BASE_URL + add
    # print(querystring)
    # req = urllib.request.Request(querystring, headers=headers)
    # req.add_header("Authorization", "Bearer " + access_token)
    # req.add_header("User-Agent", "")
    # opener = urllib.request.build_opener()
    # resp = urllib3.urlopen(req, timeout=3)
    # raw = resp.read()
    # response = opener.open(req)
    # print(response.json())
    # print(vars(response))
    # raw = response.data
    # print(raw)
    # print(vars(raw))
    # json_obj = json.loads(raw)['response']['lyrics']
    # print(raw)
    # json_obj = json.loads(raw)['response']['']

    # url = BASE_URL + add
    # print(url)
    # response = requests.get(url = url)
    # html = bs(response.text, "html.parser")
    # # print(html)
    # print(html.find("div", class_="lyrics"))
    # lyrics = html.find("div", class_="lyrics").get_text()
    # return lyrics
    lyrics = genius.search_song(x).lyrics
    formatted_lyrics = lyrics.replace('\r', '').replace('[', '').replace(']', '').strip()
    formatted_lyrics = f"""{formatted_lyrics}"""

    return formatted_lyrics

    

create()
# print(list(songs.columns))
# response = genius.search_song(songs.iloc[0]['song'])
# print()
# print(vars(response))
# print(global_songs)
# get_lyrics(songs.iloc[0]['song'])
songs['lyrics'] = songs['song'].apply(lambda x: [get_lyrics(x)])
# songs['formatted_lyrics'] = songs['song'].apply(lambda x: [genius.search_song(x).lyrics])
print(songs)



