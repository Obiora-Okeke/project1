import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from basic import app, db

class artistFormTests(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def helper(self, artist, username, name):
        return self.app.post('/spotify-generator', data=dict(artist:artist, username:username, playlist_name:name), follow_redirects=True)
    
    def test_valid_form_submission(self):
        response = self.helper('Drake', 'miltonjz513', 'PlaylistName')
        self.assertEqual(response.status_code, 200)

class registrationFormTests(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def register(self, username, password, confirm_password):
        return self.app.post('/register', data=dict(username:username, password:password, confirm_password:confirm_password), follow_redirects=True)
    
    def test_valid_registration(self):
        response = self.register('newUser', 'password1234', 'password1234')
        self.assertEqual(response.status_code, 200)

class loginFormTests(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def register(self, username, password, confirm_password):
        return self.app.post('/register', data=dict(username:username, password:password, confirm_password:confirm_password), follow_redirects=True)
    
    def login(self, username, password):
        return self.app.post('/login', data=dict(username:username, password:password), follow_redirects=True)
    
    def test_valid_login(self):
        response1 = self.register('newUser', 'password1234', 'password1234') # Creates the user
        self.assertEqual(response1.status_code, 200)
        response2 = self.login('newUser', 'password1234') # Logs in as new user
        self.assertEqual(response2.status_code, 200) 
    

if __name__ == "__main__":
        unittest.main()
