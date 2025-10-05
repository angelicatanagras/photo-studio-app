from flask import render_template, redirect, url_for, flash, request
from urllib.parse import urlparse
from . import admin_bp
from ...models.user import User, Role
from ...forms.auth import LoginForm
from ...services.auth_service import login_user, logout_user, is_authenticated, get_current_user, role_required


@admin_bp.route('/', methods=['GET', 'POST'])
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login - only allows admin role"""
    if is_authenticated():
        user = get_current_user()
        if user and user.get('role_name') == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif user and user.get('role_name') == 'photographer':
            return redirect(url_for('photographer.dashboard'))
        elif user and user.get('role_name') == 'customer':
            return redirect(url_for('customer.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and User.check_password(user.password_hash, form.password.data):
            # Check if user is an admin
            role = Role.get_by_id(user.role_id)

            if role and role['name'] != 'admin':
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
@role_required('admin')
def dashboard():
    """Admin dashboard - requires admin role"""
    user = get_current_user()

    # Get statistics
    all_users = User.get_all()
    customers = [u for u in all_users if Role.get_by_id(u.role_id)['name'] == 'customer']
    photographers = [u for u in all_users if Role.get_by_id(u.role_id)['name'] == 'photographer']
    admins = [u for u in all_users if Role.get_by_id(u.role_id)['name'] == 'admin']

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
@role_required('admin')
def users():
    """List all users - requires admin role"""
    all_users = User.get_all()
    users_with_roles = []

    for user in all_users:
        role = Role.get_by_id(user.role_id)
        users_with_roles.append({
            'user': user,
            'role': role['name'] if role else 'unknown'
        })

    return render_template(
        'admin/users.html',
        title='Manage Users',
        users=users_with_roles
    )
