from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo



class ArtistForm(FlaskForm):
    artist = StringField('Artist', validators=[DataRequired()])
    username = StringField('Spotify Username', validators=[DataRequired()])
    playlist_name = StringField('Playlist Name', validators=[DataRequired()])
    submit = SubmitField('Generate Playlist')