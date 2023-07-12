from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
# from make_album import playlist_id


app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = '626423b656a4f6851a5cbece30f78108'

@app.route("/")
@app.route("/home")
def home():
  return render_template('home.html', subtitle='Home', text='This is home page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)
@app.route("/spotify-generator")
def spotify_generator():
   return render_template('spotify_generator.html', title='Spotify Playlist Generator')

@app.route('/success', methods=['GET', 'POST'])
def playlist_created():
  return render_template('success.html', title='Playlist Created')


if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")