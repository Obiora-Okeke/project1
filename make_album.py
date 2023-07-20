from list_songs import CLIENT_ID, CLIENT_SECRET, scope
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

def create_playlist(username, playlist_name, songs):
    # global x
    token = util.prompt_for_user_token(username=username, 
                                    scope=scope, 
                                    client_id=CLIENT_ID,
                                    client_secret=CLIENT_SECRET, 
                                    redirect_uri='https://example.com')
    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print('cannot get token')
    user = sp.user(username)
    playlist = sp.user_playlist_create(username, playlist_name, public=True, collaborative=False, description = 'recs')
    playlist_id = playlist['id']
    x = playlist_id
    track_uris = songs['uri'].tolist()
    sp.playlist_add_items(playlist_id, track_uris)
    print(f"Playlist '{playlist_name}' created successfully with {len(songs)} songs.")
    return playlist_id


