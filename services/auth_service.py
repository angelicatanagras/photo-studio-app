from functools import wraps
from flask import session, redirect, url_for, flash, request
from ..database import fetch_one


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
        """SELECT u.*, r.name as role_name
           FROM users u
           JOIN roles r ON u.role_id = r.id
           WHERE u.id = %s""",
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
    return dict(
        current_user=get_current_user(),
        is_authenticated=is_authenticated()
    )
