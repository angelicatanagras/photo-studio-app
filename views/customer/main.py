from flask import render_template, request
from . import customer_bp
from ...models.photographer import Photographer
from ...models.booking import ServiceCategory
from ...services.auth_service import login_required, get_current_user


@customer_bp.route('/')
@customer_bp.route('/index')
def index():
    photographers = Photographer.get_all()

    service_categories = ServiceCategory.get_all()

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
