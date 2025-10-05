"""
Custom authentication utilities to replace Flask-Login.
Provides session-based authentication with login/logout functionality.
"""
from functools import wraps
from flask import session, redirect, url_for, flash, request
from ..database import fetch_one


def login_user(user_id, remember=False):
    """
    Log in a user by storing their ID in the session.

    Args:
        user_id (int): The user's database ID
        remember (bool): Whether to make the session permanent (not implemented yet)
    """
    session['user_id'] = user_id
    session.permanent = remember


def logout_user():
    """Log out the current user by clearing the session."""
    session.clear()


def get_current_user():
    """
    Get the current logged-in user from the session.

    Returns:
        dict or None: User dictionary if logged in, None otherwise
    """
    user_id = session.get('user_id')
    if user_id is None:
        return None

    # Fetch user from database
    user = fetch_one(
        """
        SELECT u.*, r.name as role_name
        FROM users u
        JOIN roles r ON u.role_id = r.id
        WHERE u.id = %s
        """,
        (user_id,)
    )
    return user


def is_authenticated():
    """
    Check if a user is currently authenticated.

    Returns:
        bool: True if user is logged in, False otherwise
    """
    return 'user_id' in session


def login_required(f):
    """
    Decorator to require login for a view.

    Usage:
        @app.route('/protected')
        @login_required
        def protected_view():
            return "This requires login"
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """
    Decorator to require specific role(s) for a view.

    Args:
        *roles: One or more role names required to access the view

    Usage:
        @app.route('/admin')
        @role_required('admin')
        def admin_view():
            return "Admin only"

        @app.route('/photos')
        @role_required('photographer', 'admin')
        def photographer_view():
            return "Photographers and admins"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not is_authenticated():
                flash('Please log in to access this page.', 'warning')
                # Redirect to appropriate login based on role
                if 'admin' in roles:
                    return redirect(url_for('admin.login', next=request.url))
                elif 'photographer' in roles:
                    return redirect(url_for('auth.photographer_login', next=request.url))
                else:
                    return redirect(url_for('auth.login', next=request.url))

            user = get_current_user()
            if user and user.get('role_name') not in roles:
                flash('You do not have permission to access this page.', 'danger')
                # Redirect to user's appropriate dashboard
                if user.get('role_name') == 'admin':
                    return redirect(url_for('admin.dashboard'))
                elif user.get('role_name') == 'photographer':
                    return redirect(url_for('photographer.dashboard'))
                else:
                    return redirect(url_for('customer.index'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Context processor to make current_user available in templates
def inject_current_user():
    """
    Template context processor to inject current_user into all templates.
    This should be registered with the Flask app.

    Usage in app.py:
        app.context_processor(inject_current_user)
    """
    return dict(
        current_user=get_current_user(),
        is_authenticated=is_authenticated()
    )
