from flask import Flask, render_template, url_for, flash, redirect, request
from forms import ArtistForm
from flask_behind_proxy import FlaskBehindProxy
from list_songs import api_call, json_to_dataframe, top_songs_call, dataframe_to_database
from genius import get_genius_info, set_songs_df
from make_album import create_playlist
import pandas as pd


app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = '626423b656a4f6851a5cbece30f78108'
# x = ''

x=''
@app.route("/")
@app.route("/home")
def home():
  return render_template('home.html', subtitle='Home', text='This is home page')

# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit(): # checks if entries are valid
#         flash(f'Account created for {form.username.data}!', 'success')
#         return redirect(url_for('home')) # if so - send to home page
#     return render_template('register.html', title='Register', form=form)
# @app.route("/spotify-generator")

@app.route("/spotify-generator", methods=['GET', 'POST'])
def spotify_generator():
    # global x
    print('print pls')
    return render_template('spotify_generator.html', title='Spotify Playlist Generator')


@app.route('/success', methods=['GET', 'POST'])
def playlist_created():
  form = ArtistForm()
  global x
  if request.method == "POST":
      artist_name = request.form.get('artist')
      username = request.form.get('username')
      playlist_name = request.form.get('playlist')
      print('artist:' , artist_name)
      print('playlist:', playlist_name)
      print('username:', username)
      dat = api_call(artist_name)
      adf = json_to_dataframe(dat)
      rel_artists = adf['name'].tolist()
      songs = pd.DataFrame()
      for ar in rel_artists[:5]:
          ar_songs = top_songs_call(ar)
          ar_songs_df = pd.DataFrame(ar_songs)
          songs = pd.concat([songs, ar_songs_df])
      set_songs_df(songs)
      get_genius_info()
      # dataframe_to_database(songs)
      print('songs:', songs)
      song_ids = songs['song_id'].to_list()
      print(song_ids)
      x = create_playlist(username, playlist_name, songs)
      print(x)
      flash(f"Playlist '{playlist_name}' created successfully with {len(songs)} songs.", 'success')
      # return render_template('spotify_generator.html', title='Spotify Playlist Generator')
      # return redirect('/succe')
      return render_template('success.html', title='Playlist Created', playlist_id = x)
  print('x val: ', x)
  # return render_template('success.html', title='Playlist Created', playlist_id = x)


if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")