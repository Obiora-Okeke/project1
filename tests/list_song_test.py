import unittest
import requests
import sys
import os
from unittest.mock import patch
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
from list_songs import (
    get_artist_id,
    api_call,
    top_songs_call,
    json_to_dataframe,
    songs_dataframe,
)



class TestPrograms(unittest.TestCase):
    @patch('list_songs.requests.get')
    def test_get_artist_id(self, mock_get):
        # Mock the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'artists': {
                'items': [
                    {'id': '12345'}
                ]
            }
        }
        
        artist_id = get_artist_id('ArtistName')
        
        self.assertEqual(artist_id, '12345')

    @patch('list_songs.requests.get')
    def test_api_call(self, mock_get):
        # Mock the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'artists': {
                'items': [
                    {'id': '12345'},     
                ]
            }   
        }
        
        
        result = api_call('ArtistName')
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'ArtistName')

    @patch('list_songs.requests.get')
    def test_top_songs_call(self, mock_get):
        # Mock the API response
        mock_get.return_value.status_code = 200
        #mock_get.return_value.json.return_value = {
        #    'tracks': [
        #        {
        #            'artists': [{'name': 'Artist1'}],
        #            'name': 'Song1',
        #            'uri': 'spotify:track:123'
        #        },
        #        {
        #            'artists': [{'name': 'Artist2'}],
        #            'name': 'Song2',
        #            'uri': 'spotify:track:456'
        #        }
        #    ]
        #}
        mock_get.return_value.json.return_value = {
            'artists': {
                'items': [
                    {'id': '12345'}
                ]
            }
        }

        # Add another mock response for the top songs API call
        mock_get.return_value.json.side_effect = [
            {
                'tracks': [
                    {
                        'artists': [{'name': 'Artist1'}],
                        'name': 'Song1',
                        'uri': 'spotify:track:123'
                    },
                    {
                        'artists': [{'name': 'Artist2'}],
                        'name': 'Song2',
                        'uri': 'spotify:track:456'
                    }
                ]
            }
        ]

        result = top_songs_call('ArtistName')
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['artist'], 'Artist1')
        self.assertEqual(result[1]['song'], 'Song2')

    def test_json_to_dataframe(self):
        sample_data = {
            'artists': [
                {'name': 'Artist1', 'uri': 'spotify:artist:123', 'popularity': 80, 'followers': {'total': 1000}, 'id': '123'},
                {'name': 'Artist2', 'uri': 'spotify:artist:456', 'popularity': 70, 'followers': {'total': 2000}, 'id': '456'}
            ]
        }
        
        result_df = json_to_dataframe(sample_data)
        
        
        self.assertEqual(result_df.shape, (2, 5))
        self.assertEqual(result_df.iloc[0]['name'], 'Artist2')
        self.assertEqual(result_df.iloc[1]['name'], 'Artist1')

    def test_songs_dataframe(self):
        sample_data = [
            {'artist': 'Artist1', 'song': 'Song1', 'uri': 'spotify:track:123', 'track_id': '123'},
            {'artist': 'Artist2', 'song': 'Song2', 'uri': 'spotify:track:456', 'track_id': '456'}
        ]
        
        result_df = songs_dataframe(sample_data)
        
        # Assert the correctness of the DataFrame (you can adjust the values based on your actual expected output)
        self.assertEqual(result_df.shape, (2, 4))
        self.assertEqual(result_df.iloc[0]['artist'], 'Artist1')
        self.assertEqual(result_df.iloc[1]['song'], 'Song2')

if __name__ == '__main__':
    unittest.main()