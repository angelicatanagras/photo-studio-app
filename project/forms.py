from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, TextAreaField, SelectField, DateField, IntegerField, FloatField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from .models import User, Category
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

class PortfolioUploadForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(message='Title is required'),
        Length(min=2, max=100, message='Title must be between 2 and 100 characters')
    ])
    caption = TextAreaField('Caption', validators=[
        Optional(),
        Length(max=500, message='Caption cannot exceed 500 characters')
    ])
    portfolio_image = FileField('Portfolio Image', validators=[
        FileRequired(message='Please select an image to upload'),
        FileAllowed(['png', 'jpg', 'jpeg', 'gif', 'webp'], 
                   message='Only image files are allowed (PNG, JPG, JPEG, GIF, WEBP)')
    ])
    submit = SubmitField('Upload Image')

class PhotographerBioForm(FlaskForm):
    """Form for updating photographer bio/summary"""
    bio = TextAreaField('Bio/Summary', validators=[
        Optional(),
        Length(max=1000, message='Bio cannot exceed 1000 characters')
    ])
    submit = SubmitField('Update Bio')

    
class SinglePackageForm(FlaskForm):
    """Form for creating/updating a single package"""
    package_name = SelectField('Package Type', 
                                choices=[('', 'Select Package Type'),
                                        ('Basic', 'Basic'), 
                                        ('Standard', 'Standard'), 
                                        ('Premium', 'Premium')],
                                validators=[DataRequired(message='Package type is required')])
    category = SelectField('Category', 
                          choices=[],
                          coerce=int,
                          validators=[DataRequired(message='Category is required')])
    price = FloatField('Price ($)', validators=[
        DataRequired(message='Price is required'),
        NumberRange(min=0, max=10000, message='Price must be between $0 and $10,000')
    ])
    inclusions = TextAreaField('What\'s Included', validators=[
        DataRequired(message='Please describe what\'s included in this package'),
        Length(min=10, max=500, message='Inclusions must be between 10 and 500 characters')
    ])
    submit = SubmitField('Create Package')
    
    def __init__(self, *args, **kwargs):
        super(SinglePackageForm, self).__init__(*args, **kwargs)
        # Populate category choices from database
        categories = Category.get_all()
        category_choices = [(0, 'Select Category')] + [(c.id, c.category_name) for c in categories]
        self.category.choices = category_choices    