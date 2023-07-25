import unittest
from unittest.mock import patch, MagicMock
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from genius import get_lyrics, get_annotations

class GeniusAPITest(unittest.TestCase):
    @patch('genius.Genius.search_song')
    def test_get_lyrics(self, mock_search_song):
        # Mock the response from the Genius API
        mock_song = MagicMock()
        mock_song.url = 'https://genius.com/song-url'
        mock_song.lyrics = "Sample lyrics [Chorus] Sample lyrics [Verse 1]"

        # Set the return value of the search_song function to the mock_song
        mock_search_song.return_value = mock_song

        # Call the function under test
        lyrics = get_lyrics('Sample Song')

        # Verify the interactions and assertions
        mock_search_song.assert_called_once_with('Sample Song')
        self.assertEqual(lyrics, "Sample lyrics [Chorus] Sample lyrics [Verse 1]")

    @patch('genius.Genius.referents')
    def test_get_annotations(self, mock_referents):
        # Mock the response from the Genius API
        mock_referent = MagicMock()
        mock_referent['referent'] = {'fragment': '[Chorus]', 'annotations': [{'body': {'plain': 'Annotation content'}}]}

        # Set the return value of the referents function to the mock_referent
        mock_referents.return_value = {'referents': [mock_referent]}

        # Call the function under test
        annotations = get_annotations(12345)

        # Verify the interactions and assertions
        mock_referents.assert_called_once_with(song_id=12345, per_page=50)
        self.assertEqual(annotations, {12345: {'[Chorus]': 'Annotation content'}})

if __name__ == '__main__':
    unittest.main()