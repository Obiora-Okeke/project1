'''
import requests
import json
import os
from pytube import YouTube
from list_songs import CLIENT_ID, CLIENT_SECRET, scope


import zipfile
import os

def download_songs(songs):
    # temporary folder for storing downloaded songs
    os.makedirs('temp_songs', exist_ok=True)

    api_key = 'AIzaSyAj39sgUo0s3BtaBdY9fUXeTYgOU5y_Eyg' 
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    track_names = songs['song'].tolist()
    print(track_names)
    for name in track_names:
        search_params = {
            'part': 'snippet',
            'q': name,
            'key': api_key,
            'maxResults': 1,
            'type': 'video'
        }

        response = requests.get(search_url, params=search_params)
        video_data = response.json()
        video_id = video_data['items'][0]['id']['videoId']

        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(youtube_url)
        video = yt.streams.filter(only_audio=True).first()

        out_file = video.download(output_path='temp_songs')

        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        print(f"{yt.title} has been successfully downloaded and saved at {new_file}.")

    # creating a zip file
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    zip_file_path = os.path.join(downloads_folder, 'downloaded_songs.zip')
    print(f"Creating zip file at {zip_file_path}...")

    with zipfile.ZipFile(zip_file_path, 'w') as myzip:
        for root, dirs, files in os.walk('temp_songs'):
            for file in files:
                myzip.write(os.path.join(root, file), arcname=file)

    # deleting temporary folder
    for file in os.listdir('temp_songs'):
        os.remove(os.path.join('temp_songs', file))
    os.rmdir('temp_songs')

'''

'''
def download_songs(songs):
        
    api_key = 'AIzaSyAj39sgUo0s3BtaBdY9fUXeTYgOU5y_Eyg' 
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    track_names = songs['song'].tolist()
    for name in track_names:

        search_params = {
            'part': 'snippet',
            'q': name,
            'key': api_key,
            'maxResults': 1,
            'type': 'video'
        }

        response = requests.get(search_url, params=search_params)

        video_data = response.json()
        video_id = video_data['items'][0]['id']['videoId']

        youtube_url = f"https://www.youtube.com/watch?v={video_id}"

        

        yt = YouTube(youtube_url)
        video = yt.streams.filter(only_audio=True).first()

        out_file = video.download(output_path=os.getcwd())

        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        print(yt.title + " has been successfully downloaded.")
        print(yt.title)

tracks = ['Candy Shop', 'Dior', 'Demeanor']
download_songs(tracks)

'''

from concurrent.futures import ThreadPoolExecutor
import requests
from requests.sessions import Session
import os
from pytube import YouTube
from list_songs import CLIENT_ID, CLIENT_SECRET, scope
import zipfile

def download_song(name, session):
    api_key = 'AIzaSyAj39sgUo0s3BtaBdY9fUXeTYgOU5y_Eyg'
    search_url = 'https://www.googleapis.com/youtube/v3/search'

    search_params = {
        'part': 'snippet',
        'q': name,
        'key': api_key,
        'maxResults': 1,
        'type': 'video'
    }

    response = session.get(search_url, params=search_params)
    video_data = response.json()
    video_id = video_data['items'][0]['id']['videoId']

    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    yt = YouTube(youtube_url)
    video = yt.streams.filter(only_audio=True).first()

    out_file = video.download(output_path='temp_songs')

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    print(f"{yt.title} has been successfully downloaded and saved at {new_file}.")

def download_songs(songs,pl_name):
    os.makedirs('temp_songs', exist_ok=True)

    track_names = songs['song'].tolist()
    with Session() as session:
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(lambda song: download_song(song, session), track_names)

    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    zip_file_path = os.path.join(downloads_folder, f'{pl_name}.zip')

    with zipfile.ZipFile(zip_file_path, 'w') as myzip:
        for root, dirs, files in os.walk('temp_songs'):
            for file in files:
                myzip.write(os.path.join(root, file), arcname=file)

    for file in os.listdir('temp_songs'):
        os.remove(os.path.join('temp_songs', file))
    os.rmdir('temp_songs')
