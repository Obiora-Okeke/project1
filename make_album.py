from list_songs import BASE_URL, client_id, access_token
# from spotify_recs import adf
import requests

def create_playlist(self):
    data = requests.dumps({
        'name'          : 'Recommendations',
        'description'   : 'Recommended tracks',
        'public'        :  True,

    })

    url = f"{BASE_URL}users/{client_id}/playlists"
    response = requests.post(url, data)
    response_json = response.json()

    playlist_id = response_json['id']
    playlist = 

def post_api_request(url, data):
    response = requests.post(
        url, 
        data,
        headers = {
            'Content-Type'  : 'application/json',
            'Authorization' : 'Bearer {token}'.format(token=access_token)
        }

    )


