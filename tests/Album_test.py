import unittest
from unittest.mock import patch, MagicMock
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from make_album import create_playlist

class CreatePlaylistTest(unittest.TestCase):
    @patch('make_album.util.prompt_for_user_token')
    @patch('make_album.spotipy.Spotify')
    def test_create_playlist(self, mock_spotify, mock_prompt_for_user_token):
        # Prepare mock objects and data
        username = 'miltonjz513'
        playlist_name = 'test_playlist'
        songs = [
            {'uri': 'spotify:track:123456'},
            {'uri': 'spotify:track:789012'}
        ]

        # Mock the prompt_for_user_token to return a token
        mock_prompt_for_user_token.return_value = 'test_token'

        # Create a MagicMock object for Spotify
        mock_sp = MagicMock()

        # Set the return values for the Spotify mock
        mock_sp.return_value.user.return_value = MagicMock()
        mock_sp.return_value.user_playlist_create.return_value = {'id': 'test_playlist_id'}
        mock_sp.return_value.playlist_add_items.return_value = MagicMock()

        # Assign the Spotify mock to the SpotifyOAuth instance
        mock_spotify.return_value = mock_sp

        # Call the function under test
        result = create_playlist(username, playlist_name, songs)

        # Verify the interactions and assertions
        mock_prompt_for_user_token.assert_called_once_with(
            username=username,
            scope='playlist-modify-public',
            client_id='a166e30a445349bfbea9de8fc9f5cde3',  # Replace with your actual client ID
            client_secret='379c776f28824e80863ea3d8155fe6ae',  # Replace with your actual client secret
            redirect_uri='https://example.com'
        )
        mock_sp.assert_called_once_with(auth='test_token')
        mock_sp.return_value.user.assert_called_once_with(username)
        mock_sp.return_value.user_playlist_create.assert_called_once_with(
            username,
            playlist_name,
            public=True,
            collaborative=False,
            description='recs'
        )
        mock_sp.return_value.playlist_add_items.assert_called_once_with(
            'test_playlist_id',
            ['spotify:track:123456', 'spotify:track:789012']
        )

        self.assertEqual(result, 'test_playlist_id')


if __name__ == '__main__':
    unittest.main()