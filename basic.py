from flask import Flask, render_template, url_for, flash, redirect, request, session
from forms import ArtistForm, RegistrationForm, LoginForm
from flask_behind_proxy import FlaskBehindProxy
from list_songs import api_call, json_to_dataframe, top_songs_call
from make_album import create_playlist
import pandas as pd
import functools
from flask_sqlalchemy import SQLAlchemy

x = ''

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username is already taken. Please choose a different one.', 'danger')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash('Login successful.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/success', methods=['GET', 'POST'])
@require_login
def playlist_created():
    form = ArtistForm()
    global x
    if request.method == "POST":
        artist_name = request.form.get('artist')
        username = session['username']
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
        flash(f"Playlist '{playlist_name}' created successfully with {len(songs)} songs.", 'success')
        track_ids = songs['track_id'].tolist()
        return render_template('success.html', title='Playlist Created', playlist_id=x, track_ids=track_ids)

@app.route('/account')
@require_login
def account():
    username = session['username']
    return render_template('account.html', title='Account', username=username)

if __name__ == '__main__':
    create_tables()  # Create the database tables
    app.run(debug=True, host="0.0.0.0")
