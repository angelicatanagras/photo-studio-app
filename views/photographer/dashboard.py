from flask import render_template
from . import photographer_bp
from ...services.auth_service import login_required, get_current_user


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
