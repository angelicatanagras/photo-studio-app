from flask import render_template, redirect, url_for, flash, request
from urllib.parse import urlparse
from . import auth_bp
from ..models.user import User, Role
from ..models.photographer import Customer, Photographer
from ..forms.auth import LoginForm, RegistrationForm
from ..services.auth_service import login_user, logout_user, is_authenticated, get_current_user


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Customer login - only allows customer role"""
    if is_authenticated():
        user = get_current_user()
        if user and user.get('role_name') == 'customer':
            return redirect(url_for('customer.index'))
        elif user and user.get('role_name') == 'photographer':
            return redirect(url_for('photographer.dashboard'))
        elif user and user.get('role_name') == 'admin':
            return redirect(url_for('admin.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and User.check_password(user.password_hash, form.password.data):
            # Check if user is a customer
            user_dict = get_current_user() if is_authenticated() else None
            role = Role.get_by_id(user.role_id)

            if role and role['name'] != 'customer':
                if role['name'] == 'admin':
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
    """Photographer login - only allows photographer role"""
    if is_authenticated():
        user = get_current_user()
        if user and user.get('role_name') == 'photographer':
            return redirect(url_for('photographer.dashboard'))
        elif user and user.get('role_name') == 'customer':
            return redirect(url_for('customer.index'))
        elif user and user.get('role_name') == 'admin':
            return redirect(url_for('admin.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and User.check_password(user.password_hash, form.password.data):
            # Check if user is a photographer
            role = Role.get_by_id(user.role_id)

            if role and role['name'] != 'photographer':
                if role['name'] == 'admin':
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
    """Customer registration - creates customer role and profile"""
    if is_authenticated():
        user = get_current_user()
        if user and user.get('role_name') == 'customer':
            return redirect(url_for('customer.index'))
        elif user and user.get('role_name') == 'photographer':
            return redirect(url_for('photographer.dashboard'))
        elif user and user.get('role_name') == 'admin':
            return redirect(url_for('admin.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Get or create customer role
            customer_role = Role.get_by_name('customer')
            if not customer_role:
                customer_role = Role.create('customer')

            # Create user
            user = User.create(
                email=form.email.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                role_id=customer_role['id']
            )

            # Create customer profile
            if user:
                Customer.create(user_id=user.id)

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('auth/register.html', title='Customer Registration', form=form)

    return render_template('auth/register.html', title='Customer Registration', form=form)


@auth_bp.route('/photographer/register', methods=['GET', 'POST'])
def photographer_register():
    """Photographer registration - creates photographer role and profile"""
    if is_authenticated():
        user = get_current_user()
        if user and user.get('role_name') == 'photographer':
            return redirect(url_for('photographer.dashboard'))
        elif user and user.get('role_name') == 'customer':
            return redirect(url_for('customer.index'))
        elif user and user.get('role_name') == 'admin':
            return redirect(url_for('admin.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Get or create photographer role
            photographer_role = Role.get_by_name('photographer')
            if not photographer_role:
                photographer_role = Role.create('photographer')

            # Create user
            user = User.create(
                email=form.email.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                role_id=photographer_role['id']
            )

            # Create photographer profile
            if user:
                Photographer.create(user_id=user.id)

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