'''Flask form for user registration'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Length, Email, DataRequired, EqualTo

from market.model import User


class Form(FlaskForm):
    '''User Registration | Sign-in and Sign-up'''

    # check whether email already exist in the DB
    def validate_email(self, form_field_email):
        '''Field vaildation | email should be unique'''
        user = User.query.filter_by(email=form_field_email.data).first()
        if user:
            raise ValidationError(message="Email already exists!")


    username = StringField(
        label='Username', description="Username",
        validators=[Length(min=2, max=30), DataRequired()]
    )
    email = StringField(
        label='Email', description="Email address",
        validators=[Email(), DataRequired()]
    )
    password = PasswordField(
        label='Password', description="Password",
        validators=[Length(min=6), DataRequired()]
    )
    confirm_password = PasswordField(
        label='Confirm password', description="Confirm password",
        validators=[EqualTo(fieldname='password'), DataRequired()]
    )
    submit = SubmitField(label='Submit')



class LoginForm(FlaskForm):
    '''Login form'''
    email = StringField(
        label='Email Address',
        validators=[Email(), DataRequired()]
    )
    password = PasswordField(
        label='Password',
        validators=[DataRequired()]
    )
    submit = SubmitField(label='Login')