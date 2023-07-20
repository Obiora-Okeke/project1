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

def set_songs_df(df):
    global songs
    songs = df

def get_lyrics(x='The Box'):
    global genius_song_ids
    song = genius.search_song(x)
    URL = song.url
    page = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15'})
    soup = BeautifulSoup(page.content, "html.parser")
    text = soup.select_one('div[class^="Lyrics__Container"], .lyrics').get_text(strip=True, separator='\n')
    # print(text)

    # song = genius.search_song(x)
    genius_song_ids.append(song.id)
    # lyrics = song.lyrics
    # formatted_lyrics = lyrics.replace('\r', '').replace('[', '').replace(']', '').strip()
    # formatted_lyrics = f"""{formatted_lyrics}"""
    return text

def get_annotations(x):
    request = genius.referents(song_id=x, per_page=50)
    # print('requests:', request)
    # print(request)
    annotation_ids = [y['id'] for x in request['referents'] for y in x['annotations']]
    # print(annotation_ids)
    # check = [annotation_ids[0]]
    # trial = genius.referent(check)
    # print(trial['referent']['fragment'])
    # annotations = trial['referent']['annotations']
    # for annotation in annotations:
    #     content = annotation['body']['plain']
    #     annotation_dict['annotation_id'] = [fragment, annotation]
    # print(content)
    # # print(type(annotation))
    # print(vars(annotation))
    # print(trial['referent']['annotations'])
    

    # annotations = [y for x in request['referents'] for y in x['annotations']]
    # print('annotations no: ', len(annotations))
    # print(annotations)
    # fragments = [y['fragment'] for y in request['referents']]
    # print(fragments)
    # print('fragments no: ', len(fragments))
    annotation_dict = {}
    # count = 0
    # for annotation in annotations:
    #     fragment = fragments[count]
    #     annotation_dict[annotation['id']] = [fragment, annotation['body']]
    #     count += 1
    # referents = genius.referent(annotation_ids)
    # print(referents[0])
    for annotation_id in annotation_ids:
        referent = genius.referent([annotation_id])
        fragment = referent['referent']['fragment']
        annotations = referent['referent']['annotations']
        for annotation in annotations:
            content = annotation['body']['plain']
            annotation_dict[annotation_id] = [fragment, content]
    print(annotation_dict)
    return annotation_dict

#fragment: portion of lyrics being annotated
def create_annotation(text, webpage, referent):
    genius.create_annotation(annotation=text, raw_annotable=webpage, fragment=referent)

def delete_annotation(id):
    genius.delete_annotation(annotation_id = id)

def downvote_annotation(id):
    genius.downvoteannotation(annotation_id = id)

def upvote_annotation(id):
    genius.upvote_annotation(annotation_id = id)

def get_genius_info():
    songs['lyrics'] = songs['song'].apply(lambda x: [get_lyrics(x)])
    songs['genius_id'] = genius_song_ids
    songs['annotations'] = songs['genius_id'].apply(lambda x: [get_annotations(x)])

# create()

song = genius.search_song('Ransom')
get_annotations(song.id)
# print(vars(song))
# request = genius.referents(song_id=5068155, per_page=50)
# print(request)


#TO CREATE ANNOTATION
# annotation = input('Create annotation: ')
#fragment: referent/ lyric portion being annotated
# genius.create_annotation(annotation, raw_annotable= '/lyrics', fragment = '')

# songs['lyrics'] = songs['song'].apply(lambda x: [get_lyrics(x)])
# songs['genius_id'] = genius_song_ids
# songs['annotations'] = songs['genius_id'].apply(lambda x: [get_annotations(x)])
# songs['formatted_lyrics'] = songs['song'].apply(lambda x: [genius.search_song(x).lyrics])
# print(songs)



