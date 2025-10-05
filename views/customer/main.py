from flask import render_template, request
from . import customer_bp
from ...models.photographer import Photographer
from ...models.booking import ServiceCategory
from ...services.auth_service import login_required, get_current_user


@customer_bp.route('/')
@customer_bp.route('/index')
def index():
    """Homepage with photographer listings"""
    # Get all photographers with their related data
    photographers = Photographer.get_all()

    # Get all service categories
    service_categories = ServiceCategory.get_all()

    # Get unique locations from photographers
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
    """Session package selection page with static data for preview"""
    return render_template('customer/session_package.html',
                         title='Select Package')


@customer_bp.route('/checkout')
def checkout():
    """Checkout page with static data for preview"""
    return render_template('customer/checkout.html',
                         title='Checkout')


@customer_bp.route('/success')
def success_page():
    """Success/confirmation page with static data for preview"""
    return render_template('customer/success_page.html',
                         title='Booking Success')
