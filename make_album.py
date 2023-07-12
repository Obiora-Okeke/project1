from list_songs import CLIENT_ID, CLIENT_SECRET, scope, songs
# from spotify_recs import adf
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
# from flask import Flask, render_template, url_for, flash, redirect, request

# app = Flask(__name__)

# @app.route('/')
def username_playlistname():
    username = input("Enter your Spotify username: ")
    playlist_name = input("Enter the playlist name: ")
    return username, playlist_name


def create_playlist(username, playlist_name, songs):
    user = sp.user(username)
    playlist = sp.user_playlist_create(username, playlist_name, public=True, collaborative=False, description = 'recs')
    playlist_id = playlist['id']
    track_uris = songs['uri'].tolist()
    sp.playlist_add_items(playlist_id, track_uris)

    print(f"Playlist '{playlist_name}' created successfully with {len(songs)} songs.")

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    # username = input("Enter your Spotify username: ")
    # playlist_name = input("Enter the playlist name: ")
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
    # app.add_url_rule('/', create_playlist)
    # app.run()
    
