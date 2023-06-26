import requests
import pprint

client_id = "ce303767105943e9b563c582c546bcdf"
client_secret = "4f77f234a135413787ba25237ed8e819"

AUTH_URL = 'https://accounts.spotify.com/api/token'

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
})

auth_response_data = auth_response.json()

access_token = auth_response_data['access_token']

headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}


BASE_URL = 'https://api.spotify.com/v1/'
artist_id = input('Enter artist id: ')
r = requests.get(BASE_URL + 'artists/' + artist_id + '/related-artists', headers=headers)
pprint.pprint(r.json())