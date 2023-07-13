from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# class RegistrationForm(FlaskForm):
#     username = StringField('Username',
#                            validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password',
#                                      validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Sign Up')

class ArtistForm(FlaskForm):
    artist = StringField('Artist', validators=[DataRequired()])
    username = StringField('Spotify Username', validators=[DataRequired()])
    playlist_name = StringField('Playlist Name', validators=[DataRequired()])
    submit = SubmitField('Generate Playlist')