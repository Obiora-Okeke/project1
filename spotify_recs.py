import requests
import pandas as pd
import sqlalchemy as db
import pprint

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
artist_id = input('Enter artist id: ')
r = requests.get(BASE_URL + 'artists/' + artist_id + '/related-artists',
                 headers=headers)
data = r.json()

dataframe_name = pd.DataFrame.from_dict(data['artists'])
urls = dataframe_name['external_urls'].map(lambda x: x.get('spotify', 'N/A'))
dataframe_name['external_urls'] = urls
fol = dataframe_name['followers'].map(lambda x: x.get('total', 'N/A'))
dataframe_name['followers'] = fol
actual_data_frame = dataframe_name[['name', 'external_urls', 'popularity',
                                    'followers']].sort_values(
                                        'followers', ascending=False
                                    )

engine = db.create_engine('sqlite:///actual_data_frame.db')
actual_data_frame.to_sql(
    'table_name', con=engine, if_exists='replace', index=False
)
with engine.connect() as connection:
    connect = connection.execute(db.text("SELECT * FROM table_name;"))
    query_result = connect.fetchall()
    print(pd.DataFrame(query_result))
