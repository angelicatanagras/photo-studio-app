from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, TextAreaField, SelectField, DateField, IntegerField, FloatField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from datetime import datetime, time
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
    def validate_event_date(self, field):
        """Validate that event date cannot be in the past"""
        if field.data and field.data < datetime.now().date():
            raise ValidationError('Event date cannot be in the past.')
    
    def validate_event_time(self, field):
        """Validate that if today is selected, time cannot be in the past"""
        if self.event_date.data == datetime.now().date() and field.data:
            try:
                selected_time = datetime.strptime(field.data, '%H:%M').time()
                current_time = datetime.now().time()
                if selected_time <= current_time:
                    raise ValidationError('Selected time has already passed for today.')
            except ValueError:
                raise ValidationError('Invalid time format.')

    package_id = HiddenField('Package ID', validators=[DataRequired()])
    photographer_id = HiddenField('Photographer ID', validators=[DataRequired()])
    event_date = DateField('Event Date', 
                          validators=[DataRequired()],
                          render_kw={"min": datetime.now().date().isoformat()})
    event_time = SelectField('Event Time', choices=[
        ('09:00', '9:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('12:00', '12:00 PM'),
        ('13:00', '1:00 PM'),
        ('14:00', '2:00 PM'),
        ('15:00', '3:00 PM'),
        ('16:00', '4:00 PM'),
        ('17:00', '5:00 PM')
    ], validators=[DataRequired()])
    pax = IntegerField('Number of Pax', validators=[DataRequired(), NumberRange(min=1, max=50)])
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

class ProfilePictureForm(FlaskForm):
    """Form for uploading profile picture"""
    profile_picture = FileField('Profile Picture', validators=[
        FileRequired(message='Please select an image to upload'),
        FileAllowed(['png', 'jpg', 'jpeg', 'gif', 'webp'], 
                   message='Only image files are allowed (PNG, JPG, JPEG, GIF, WEBP)')
    ])
    submit = SubmitField('Upload Picture')
    
    
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

class CategoryForm(FlaskForm):
    """Form for creating a new category"""
    category_name = StringField('Category Name', validators=[
        DataRequired(message='Category name is required'),
        Length(min=2, max=25, message='Category name must be between 2 and 25 characters')
    ])
    description = StringField('Description', validators=[
        Optional(),
        Length(max=100, message='Description cannot exceed 100 characters')
    ])
    submit = SubmitField('Add Category')    

class CheckoutForm(FlaskForm):
    """Form for checkout with contact and payment information"""
    
    # Contact Information
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=50, message='First name must be between 2 and 50 characters')
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=50, message='Last name must be between 2 and 50 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    phone = StringField('Phone Number', validators=[
        DataRequired(message='Phone number is required')
    ])
    
    # Payment Information
    card_number = StringField('Card Number', validators=[
        DataRequired(message='Card number is required'),
        Length(min=13, max=19, message='Card number must be between 13 and 19 digits')
    ])
    expiry_date = StringField('Expiry Date', validators=[
        DataRequired(message='Expiry date is required')
    ])
    cvc = StringField('CVC', validators=[
        DataRequired(message='CVC is required'),
        Length(min=3, max=4, message='CVC must be 3 or 4 digits'),
        
    ])
    cardholder_name = StringField('Cardholder Name', validators=[
        DataRequired(message='Cardholder name is required'),
        Length(min=2, max=100, message='Cardholder name must be between 2 and 100 characters')
    ])
    
    submit = SubmitField('Place Order')