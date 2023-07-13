from list_songs import client_secret, client_id, scope
# from spotify_recs import adf
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
# from flask import Flask, render_template, url_for, flash, redirect, request

# app = Flask(__name__)

# @app.route('/')
x = ''
def create_playlist(username, playlist_name, songs):
    global x
    token = util.prompt_for_user_token(username=username, 
                                        scope=scope, 
                                        client_id=client_id,
                                        client_secret=client_secret, 
                                        redirect_uri='http://example.com')
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
