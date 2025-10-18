from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, TextAreaField, SelectField, DateField, IntegerField, FloatField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange
from .models import User
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    role = RadioField('I am a', choices=[('Customer', 'Customer'), ('Photographer', 'Photographer')],
                      default='Customer', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.get_by_email(email.data)
        if user is not None:
            raise ValidationError('Please use a different email address.')

class BookingForm(FlaskForm):
    package_id = HiddenField('Package ID', validators=[DataRequired()])
    photographer_id = HiddenField('Photographer ID', validators=[DataRequired()])
    event_date = DateField('Event Date', validators=[Optional()])
    event_time = SelectField('Event Time', choices=[
        ('9:00', '9:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('12:00', '12:00 PM'),
        ('13:00', '1:00 PM'),
        ('14:00', '2:00 PM'),
        ('15:00', '3:00 PM'),
        ('16:00', '4:00 PM')
    ], validators=[Optional()])
    pax = IntegerField('Number of Pax', validators=[Optional(), NumberRange(min=1, max=50)])
    notes = TextAreaField('Event Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Proceed to checkout')