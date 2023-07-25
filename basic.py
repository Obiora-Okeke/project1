from flask import Flask, render_template, url_for, flash, redirect, request
from forms import ArtistForm
from flask_behind_proxy import FlaskBehindProxy
from list_songs import api_call, json_to_dataframe, top_songs_call
from genius import get_lyrics
from make_album import create_playlist
import pandas as pd
from flask_modals import Modal
from flask_modals import render_template_modal
# from jinja2 import Markup

x=''
id_name_dict = {}
app = Flask(__name__)
modal = Modal(app)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '626423b656a4f6851a5cbece30f78108'

@app.route("/")
@app.route("/home")
def home():
  return render_template('home.html', subtitle='Home', text='This is home page')

@app.route("/spotify-generator", methods=['GET', 'POST'])
def spotify_generator():
    return render_template('spotify_generator.html', title='Spotify Playlist Generator')

@app.route("/about")
def about():
   return render_template('about.html', text="This is the about page.", title = 'About Page')

@app.route('/success', methods=['GET', 'POST'])
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