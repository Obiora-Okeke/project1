import requests
import pandas as pd
import sqlalchemy as db
import pprint

def get_artist_id(artist_name):
    search_response = requests.get(BASE_URL + 'search',
                                  headers=headers,
                                  params={'q': artist_name,
                                          'type': 'artist',
                                          'limit': 1})
    if search_response.status_code == 200:
        artists = search_response.json()['artists']['items']
        if artists:
            return artists[0]['id']
        else:
            print(f"No artist found with the name: {artist_name}")
    else:
        print("Error occurred while searching for the artist.")
    return None


def api_call():
    artist_name = input('Enter artist name: ')
    artist_id = get_artist_id(artist_name)
    r = requests.get(BASE_URL + 'artists/' + artist_id + '/related-artists',
                     headers=headers)
    return r.json()


def error_check(li):
    check = 'artists' in li.keys()
    if check:
        return False
    else:
        print('Error. Input working ID')
        return True


def json_to_dataframe(data):
    dataframe_name = pd.DataFrame.from_dict(data['artists'])
    urls = dataframe_name['external_urls'].map(lambda x: x.get('spotify',
                                                               'N/A'))
    dataframe_name['external_urls'] = urls
    fol = dataframe_name['followers'].map(lambda x: x.get('total', 'N/A'))
    dataframe_name['followers'] = fol
    return dataframe_name[['name', 'external_urls', 'popularity',
                           'followers']].sort_values('followers',
                                                     ascending=False)


def dataframe_to_database(frame):
    frame.to_sql(
        'table_name', con=engine, if_exists='replace', index=False
    )


pd.set_option('max_colwidth', None)
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
dat = api_call()
error_present = error_check(dat)
while error_present:
    artist_id = input('Enter artist id: ')
    r = requests.get(BASE_URL + 'artists/' + artist_id + '/related-artists',
                     headers=headers)
    dat = r.json()
    error_present = error_check(dat)
adf = json_to_dataframe(dat)
engine = db.create_engine('sqlite:///actual_data_frame.db')
dataframe_to_database(adf)

with engine.connect() as connection:
    connect = connection.execute(db.text("SELECT * FROM table_name;"))
    query_result = connect.fetchall()
    print(pd.DataFrame(query_result))
