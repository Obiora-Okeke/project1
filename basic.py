from flask import Flask, render_template, url_for, flash, redirect, request
from forms import ArtistForm
from flask_behind_proxy import FlaskBehindProxy
from list_songs import api_call, json_to_dataframe, top_songs_call
from make_album import create_playlist
from mp3 import download_songs
import pandas as pd

x=''
app = Flask(__name__)
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
      x = create_playlist(username, playlist_name, songs)
      
      download_songs(songs, playlist_name)
      flash(f"Playlist '{playlist_name}' created successfully with {len(songs)} songs.", 'success')
      track_ids = songs['track_id'].tolist()
      return render_template('success.html', title='Playlist Created', playlist_id = x, track_ids=track_ids)


if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")