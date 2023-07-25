import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from basic import app

class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_homepage(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.app.get('/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_spotify_generator(self):
        response = self.app.get('/spotify-generator', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_success(self):
        response = self.app.get('/success', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_account(self):
        response = self.app.get('/account', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_getLyrics(self):
        response = self.app.get('/get-lyrics', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()