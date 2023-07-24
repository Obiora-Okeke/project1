from flask import Flask, render_template, url_for, flash, redirect, request, session
from forms import ArtistForm, RegistrationForm, LoginForm
from flask_behind_proxy import FlaskBehindProxy
from list_songs import api_call, json_to_dataframe, top_songs_call
from genius import get_lyrics
from make_album import create_playlist
import pandas as pd
import functools
from flask_sqlalchemy import SQLAlchemy


x=''
id_name_dict = {}
app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '626423b656a4f6851a5cbece30f78108'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

def create_tables():
    with app.app_context():
        db.create_all()

def is_logged_in():
    return 'username' in session

def require_login(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if not is_logged_in():
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped_view

@app.before_request
def check_login():
    if request.endpoint and request.endpoint != 'login' and not is_logged_in():
        return redirect(url_for('login'))

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home', text='This is the home page')

@app.route("/spotify-generator", methods=['GET', 'POST'])
@require_login
def spotify_generator():
    return render_template('spotify_generator.html', title='Spotify Playlist Generator')

@app.route("/about")
def about():
   return render_template('about.html', text="This is the about page.", title = 'About Page')

@app.route('/success', methods=['GET', 'POST'])
@require_login
def playlist_created():
  form = ArtistForm()
  global x
  global id_name_dict
  if request.method == "POST":
      artist_name = request.form.get('artist')
      username = request.form.get('username')
      playlist_name = request.form.get('playlist')
      dat = api_call(artist_name)
      adf = json_to_dataframe(dat)
      rel_artists = adf['name'].tolist()
      songs = pd.DataFrame()
      for ar in rel_artists[:5]:
          ar_songs = top_songs_call(ar)
          ar_songs_df = pd.DataFrame(ar_songs)
          songs = pd.concat([songs, ar_songs_df])
      # set_songs_df(songs)
      # get_genius_info()1
      print('songs:', songs)
      # song_ids = songs['track_id'].to_list()
      song_names = songs['song'].to_list()
      # print(song_ids)
      x = create_playlist(username, playlist_name, songs)
      flash(f"Playlist '{playlist_name}' created successfully with {len(songs)} songs.", 'success')
      track_ids = songs['track_id'].tolist()
      id_name_dict = {track_ids[i]: song_names[i] for i in range(len(track_ids))}
      print(id_name_dict)
      return render_template('success.html', title='Playlist Created', playlist_id = x, track_ids=track_ids)

@app.route("/get-lyrics", methods=['GET', 'POST'])
def getLyrics():
   if request.method == "POST":
      song_id = request.form.get('id')
      print(song_id)
      song_name = id_name_dict[song_id]
      lyrics = get_lyrics(song_name)
      print(lyrics)
      return lyrics
   

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")

#. ~/.bashrc
