from flask import Flask, render_template, url_for, flash, redirect, request
# from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from forms import MyForm


app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = '626423b656a4f6851a5cbece30f78108'

@app.route("/")
@app.route("/home")
def home():
  return render_template('home.html', subtitle='Home', text='Create a Spotify Playlist')

@app.route("/second_page")
def second_page():
  return render_template('second_page.html', subtitle='Second Page', text='This is the second page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    # if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    #     username = request.form['username']
    #     password = request.form['password']
    form = MyForm()
    username = form.username.data
    playlistname = form.playlistname.data

    # if form.validate_on_submit(): # checks if entries are valid
    #     flash(f'Authenticated {form.username.data}!', 'success')
    #     return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

# @app.route('/success')

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")