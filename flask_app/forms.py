from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo,Length


class RegistrationForm(FlaskForm):

    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')


class Login(FlaskForm):

    email = StringField('Email', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])