from list_songs import BASE_URL, CLIENT_ID, CLIENT_SECRET, scope, redirect_uri, songs
# from spotify_recs import adf
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth



# def create_playlist(self):
#     data = requests.dumps({
#         'name'          : 'Recommendations',
#         'description'   : 'Recommended tracks',
#         'public'        :  True,

#     })

#     url = f"{BASE_URL}users/{client_id}/playlists"
#     response = requests.post(url, data)
#     response_json = response.json()

#     playlist_id = response_json['id']
#     playlist = 

# def post_api_request(url, data):
#     response = requests.post(
#         url, 
#         data,
#         headers = {
#             'Content-Type'  : 'application/json',
#             'Authorization' : 'Bearer {token}'.format(token=access_token)
#         }

#     )
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="https://accounts.spotify.com/authorize?client_id=a6cf4c0a0a984d06828e31a34b5f2b1c&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%2F&scope=playlist-modify-public",
                                               scope=scope))

def create_playlist(username, playlist_name, songs):
    user = sp.current_user()
    user_id = user['id']
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
    playlist_id = playlist['id']

    track_uris = songs['track_uri'].tolist()
    sp.playlist_add_items(playlist_id, track_uris)

    print(f"Playlist '{playlist_name}' created successfully with {len(songs)} songs.")

username = input("Enter your Spotify username: ")
playlist_name = input("Enter the playlist name: ")

create_playlist(username, playlist_name, songs)
