from flask import Blueprint, render_template, redirect, url_for, flash, request
from urllib.parse import urlparse
from functools import wraps
from flask import session
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import fetch_one

from .models import User, Photographer, Customer, Category
from .forms import LoginForm, RegistrationForm


# Auth service functions
def login_user(user_id, remember=False):
    session['user_id'] = user_id
    session.permanent = remember


def logout_user():
    session.clear()


def get_current_user():
    user_id = session.get('user_id')
    if user_id is None:
        return None

    user = fetch_one(
        "SELECT * FROM users WHERE id = %s",
        (user_id,)
    )
    return user


def is_authenticated():
    return 'user_id' in session


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not is_authenticated():
                flash('Please log in to access this page.', 'warning')
                if 'Admin' in roles:
                    return redirect(url_for('admin.login', next=request.url))
                elif 'Photographer' in roles:
                    return redirect(url_for('auth.photographer_login', next=request.url))
                else:
                    return redirect(url_for('auth.login', next=request.url))

            user = get_current_user()
            if user and user.get('role') not in roles:
                flash('You do not have permission to access this page.', 'danger')
                if user.get('role') == 'Admin':
                    return redirect(url_for('admin.dashboard'))
                elif user.get('role') == 'Photographer':
                    return redirect(url_for('photographer.dashboard'))
                else:
                    return redirect(url_for('customer.index'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def inject_current_user():
    return dict(
        current_user=get_current_user(),
        is_authenticated=is_authenticated()
    )


# Create Blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
customer_bp = Blueprint('customer', __name__)
photographer_bp = Blueprint('photographer', __name__, url_prefix='/photographer')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# ===== AUTH ROUTES =====

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if is_authenticated():
        user = get_current_user()
        if user and user.get('role') == 'Customer':
            return redirect(url_for('customer.index'))
        elif user and user.get('role') == 'Photographer':
            return redirect(url_for('photographer.dashboard'))
        elif user and user.get('role') == 'Admin':
            return redirect(url_for('admin.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and User.check_password(user.password_hash, form.password.data):
            if user.role != 'Customer':
                if user.role == 'Admin':
                    flash('This login is for customers only. Please use the admin login.', 'error')
                else:
                    flash('This login is for customers only. Please use the photographer login.', 'error')
                return render_template('auth/login.html', title='Customer Sign In', form=form)

            login_user(user.id, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('customer.index')
            return redirect(next_page)
        flash('Invalid email or password', 'error')

    return render_template('auth/login.html', title='Customer Sign In', form=form)


@auth_bp.route('/photographer/login', methods=['GET', 'POST'])
def photographer_login():
    if is_authenticated():
        user = get_current_user()
        if user and user.get('role') == 'Photographer':
            return redirect(url_for('photographer.dashboard'))
        elif user and user.get('role') == 'Customer':
            return redirect(url_for('customer.index'))
        elif user and user.get('role') == 'Admin':
            return redirect(url_for('admin.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and User.check_password(user.password_hash, form.password.data):
            if user.role != 'Photographer':
                if user.role == 'Admin':
                    flash('This login is for photographers only. Please use the admin login.', 'error')
                else:
                    flash('This login is for photographers only. Please use the customer login.', 'error')
                return render_template('auth/photographer_login.html', title='Photographer Sign In', form=form)

            login_user(user.id, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('photographer.dashboard')
            return redirect(next_page)
        flash('Invalid email or password', 'error')

    return render_template('auth/photographer_login.html', title='Photographer Sign In', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if is_authenticated():
        user = get_current_user()
        if user and user.get('role') == 'Customer':
            return redirect(url_for('customer.index'))
        elif user and user.get('role') == 'Photographer':
            return redirect(url_for('photographer.dashboard'))
        elif user and user.get('role') == 'Admin':
            return redirect(url_for('admin.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User.create(
                email=form.email.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                role='Customer'
            )

            if user:
                # Customer needs a postcode, using a default for now
                Customer.create(user_id=user.id, postcode='0000')

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('auth/register.html', title='Customer Registration', form=form)

    return render_template('auth/register.html', title='Customer Registration', form=form)


@auth_bp.route('/photographer/register', methods=['GET', 'POST'])
def photographer_register():
    if is_authenticated():
        user = get_current_user()
        if user and user.get('role') == 'Photographer':
            return redirect(url_for('photographer.dashboard'))
        elif user and user.get('role') == 'Customer':
            return redirect(url_for('customer.index'))
        elif user and user.get('role') == 'Admin':
            return redirect(url_for('admin.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            from datetime import datetime

            user = User.create(
                email=form.email.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                role='Photographer'
            )

            if user:
                # Photographer needs category_id, location, social_link, and availability
                # Using defaults for now - should be collected in a more detailed form
                default_category = Category.get_by_name('Portrait Photography')
                if not default_category:
                    # If no categories exist, create a default one
                    default_category = Category.create('Portrait Photography', 'Professional portrait photography')

                Photographer.create(
                    user_id=user.id,
                    category_id=default_category.id,
                    location='Location not set',
                    social_link='',
                    availability=datetime.utcnow()
                )

            flash('Registration successful! You can now log in as a photographer.', 'success')
            return redirect(url_for('auth.photographer_login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('auth/photographer_register.html', title='Photographer Registration', form=form)

    return render_template('auth/photographer_register.html', title='Photographer Registration', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('customer.index'))


# ===== CUSTOMER ROUTES =====

@customer_bp.route('/')
@customer_bp.route('/index')
def index():
    photographers = Photographer.get_all()
    service_categories = Category.get_all()

    photographer_locations = []
    for photographer in photographers:
        if photographer.location and photographer.location not in photographer_locations:
            photographer_locations.append(photographer.location)

    return render_template('customer/index.html',
                           title='Home',
                           photographers=photographers,
                           service_categories=service_categories,
                           photographer_locations=photographer_locations)


@customer_bp.route('/session/package')
def session_package():
    return render_template('customer/session_package.html',
                           title='Select Package')


@customer_bp.route('/checkout')
def checkout():
    return render_template('customer/checkout.html',
                           title='Checkout')


@customer_bp.route('/success')
def success_page():
    return render_template('customer/success_page.html',
                           title='Booking Success')


# ===== PHOTOGRAPHER ROUTES =====

@photographer_bp.route('/dashboard')
@photographer_bp.route('/admin')
def dashboard():
    """Photographer dashboard/admin page"""
    return render_template('photographer/dashboard.html',
                         title='Photographer Dashboard')


@photographer_bp.route('/gallery')
def gallery():
    """View photographer portfolio/gallery page"""
    return render_template('photographer/gallery.html',
                         title='My Gallery')


# ===== ADMIN ROUTES =====

@admin_bp.route('/', methods=['GET', 'POST'])
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if is_authenticated():
        user = get_current_user()
        if user and user.get('role') == 'Admin':
            return redirect(url_for('admin.dashboard'))
        elif user and user.get('role') == 'Photographer':
            return redirect(url_for('photographer.dashboard'))
        elif user and user.get('role') == 'Customer':
            return redirect(url_for('customer.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and User.check_password(user.password_hash, form.password.data):
            if user.role != 'Admin':
                flash('This login is for administrators only.', 'error')
                return render_template('admin/login.html', title='Admin Sign In', form=form)

            login_user(user.id, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('admin.dashboard')
            return redirect(next_page)
        flash('Invalid email or password', 'error')

    return render_template('admin/login.html', title='Admin Sign In', form=form)


@admin_bp.route('/dashboard')
@role_required('Admin')
def dashboard():
    user = get_current_user()

    all_users = User.get_all()
    customers = [u for u in all_users if u.role == 'Customer']
    photographers = [u for u in all_users if u.role == 'Photographer']
    admins = [u for u in all_users if u.role == 'Admin']

    return render_template(
        'admin/dashboard.html',
        title='Admin Dashboard',
        user=user,
        total_users=len(all_users),
        total_customers=len(customers),
        total_photographers=len(photographers),
        total_admins=len(admins)
    )


@admin_bp.route('/users')
@role_required('Admin')
def users():
    all_users = User.get_all()
    users_with_roles = []

    for user in all_users:
        users_with_roles.append({
            'user': user,
            'role': user.role
        })

    return render_template(
        'admin/users.html',
        title='Manage Users',
        users=users_with_roles
    )
