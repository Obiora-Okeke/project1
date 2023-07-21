import requests
import json
import os
from pytube import YouTube

api_key = 'AIzaSyAj39sgUo0s3BtaBdY9fUXeTYgOU5y_Eyg' 
search_url = 'https://www.googleapis.com/youtube/v3/search'

search_params = {
    'part': 'snippet',
    'q': 'The Box',
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
