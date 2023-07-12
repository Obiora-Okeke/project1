from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class MyForm(FlaskForm):
    username = StringField('Spotify Username',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Playlist Name', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')