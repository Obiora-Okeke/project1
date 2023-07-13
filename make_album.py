from list_songs import CLIENT_ID, CLIENT_SECRET, scope, songs
# from basic import playlist_name, artist_name, username
# from spotify_recs import adf
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

x = ''
def username_playlistname():
    username = input("Enter your Spotify username: ")
    playlist_name = input("Enter the playlist name: ")
    return username, playlist_name

def create_playlist(username, playlist_name, songs):
    global x
    user = sp.user(username)
    playlist = sp.user_playlist_create(username, playlist_name, public=True, collaborative=False, description = 'recs')
    playlist_id = playlist['id']
    x = playlist_id
    track_uris = songs['uri'].tolist()
    print('X1:' ,x)
    sp.playlist_add_items(playlist_id, track_uris)

    print(f"Playlist '{playlist_name}' created successfully with {len(songs)} songs.")
    # return x

username, playlist_name = username_playlistname()
token = util.prompt_for_user_token(username=username, 
                                    scope=scope, 
                                    client_id=CLIENT_ID,
                                    client_secret=CLIENT_SECRET, 
                                    redirect_uri='http://example.com/')
if token:
    sp = spotipy.Spotify(auth=token)
else:
    print('cannot get token')

create_playlist(username, playlist_name, songs)
# to_return = x


