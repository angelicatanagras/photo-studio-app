from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from urllib.parse import urlparse
from functools import wraps
from database import fetch_one
from datetime import datetime
import os
from werkzeug.utils import secure_filename


from .models import User, Photographer, Customer, Category, Booking, Cart, CartItem, Package, PortfolioItem
from .forms import LoginForm, RegistrationForm, PortfolioUploadForm, PhotographerBioForm, SinglePackageForm

# Upload configuration
UPLOAD_FOLDER = 'static/uploads/portfolio'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 5MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Session-based cart functions removed - now using database cart only


def login_user(user_id, remember=False):
    session['user_id'] = user_id
    session.permanent = remember


def logout_user():
    session.clear()


def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return fetch_one("SELECT * FROM users WHERE id = %s", (user_id,))


def is_authenticated():
    return 'user_id' in session


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated():
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not is_authenticated():
                flash('Please log in to access this page.', 'warning')
                if 'Admin' in roles:
                    return redirect(url_for('admin.login', next=request.url))
                elif 'Photographer' in roles:
                    return redirect(url_for('auth.photographer_login', next=request.url))
                return redirect(url_for('auth.login', next=request.url))
            user = get_current_user()
            if user and user.get('role') not in roles:
                flash('You do not have permission to access this page.', 'danger')
                if user.get('role') == 'Admin':
                    return redirect(url_for('admin.dashboard'))
                if user.get('role') == 'Photographer':
                    return redirect(url_for('photographer.dashboard'))
                return redirect(url_for('customer.index'))
            return f(*args, **kwargs)
        return decorated
    return decorator


def inject_current_user():
    return dict(current_user=get_current_user(), is_authenticated=is_authenticated())


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
customer_bp = Blueprint('customer', __name__)
photographer_bp = Blueprint(
    'photographer', __name__, url_prefix='/photographer')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# -- make cart badge reflect DB for logged-in customers; fallback to session when logged out


def inject_cart():
    """Inject cart count for template context - database cart only"""
    try:
        # When logged in, read from DB cart
        if is_authenticated():
            user = get_current_user()
            if user and user.get('role') == 'Customer':
                customer = Customer.get_by_user_id(user.get('id'))
                if customer:
                    cart = Cart.get_by_customer(customer.id)
                    if cart:
                        items = CartItem.get_by_cart(cart.id) or []
                        return dict(cart_count=len(items))

        # Not logged in - no cart
        return dict(cart_count=0)
    except Exception:
        return dict(cart_count=0)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if is_authenticated():
        user = get_current_user()
        if user and user.get('role') == 'Customer':
            return redirect(url_for('customer.index'))
        if user and user.get('role') == 'Photographer':
            return redirect(url_for('photographer.dashboard'))
        if user and user.get('role') == 'Admin':
            return redirect(url_for('admin.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and User.check_password(user.password_hash, form.password.data):
            if user.role != 'Customer':
                if user.role == 'Admin':
                    flash(
                        'This login is for customers only. Please use the admin login.', 'error')
                else:
                    flash(
                        'This login is for customers only. Please use the photographer login.', 'error')
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
        if user and user.get('role') == 'Customer':
            return redirect(url_for('customer.index'))
        if user and user.get('role') == 'Admin':
            return redirect(url_for('admin.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and User.check_password(user.password_hash, form.password.data):
            if user.role != 'Photographer':
                if user.role == 'Admin':
                    flash(
                        'This login is for photographers only. Please use the admin login.', 'error')
                else:
                    flash(
                        'This login is for photographers only. Please use the customer login.', 'error')
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
        if user and user.get('role') == 'Photographer':
            return redirect(url_for('photographer.dashboard'))
        if user and user.get('role') == 'Admin':
            return redirect(url_for('admin.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            selected_role = form.role.data
            user = User.create(
                email=form.email.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                role=selected_role
            )
            if user:
                if selected_role == 'Customer':
                    Customer.create(user_id=user.id, postcode='0000')
                    flash(
                        'Registration successful! You can now log in as a customer.', 'success')
                elif selected_role == 'Photographer':
                    from datetime import datetime
                    default_category = Category.get_by_name('Portrait Photography') or \
                        Category.create('Portrait Photography',
                                        'Professional portrait photography')
                    Photographer.create(
                        user_id=user.id,
                        category_id=default_category.id,
                        location='Location not set',
                        social_link='',
                        availability=datetime.utcnow()
                    )
                    flash(
                        'Registration successful! You can now log in as a photographer.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
    return render_template('auth/register.html', title='Registration', form=form)


@auth_bp.route('/photographer/register', methods=['GET', 'POST'])
def photographer_register():
    if is_authenticated():
        user = get_current_user()
        if user and user.get('role') == 'Photographer':
            return redirect(url_for('photographer.dashboard'))
        if user and user.get('role') == 'Customer':
            return redirect(url_for('customer.index'))
        if user and user.get('role') == 'Admin':
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
                default_category = Category.get_by_name('Portrait Photography') or \
                    Category.create('Portrait Photography',
                                    'Professional portrait photography')
                Photographer.create(
                    user_id=user.id,
                    category_id=default_category.id,
                    location='Location not set',
                    social_link='',
                    availability=datetime.utcnow()
                )
            flash(
                'Registration successful! You can now log in as a photographer.', 'success')
            return redirect(url_for('auth.photographer_login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
    return render_template('auth/photographer_register.html', title='Photographer Registration', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('customer.index'))


@customer_bp.route('/')
@customer_bp.route('/index')
def index():
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 8

    all_photographers = Photographer.get_all()
    total = len(all_photographers)
    total_pages = (total + per_page - 1) // per_page

    start = (page - 1) * per_page
    end = start + per_page
    photographers = all_photographers[start:end]

    # Get featured photographers with portfolio
    from project.models import PortfolioItem
    featured_photographers = Photographer.get_featured()
    for photographer in featured_photographers:
        photographer.portfolio_items = PortfolioItem.get_by_photographer(
            photographer.id)

    service_categories = Category.get_all()
    photographer_locations = []
    for p in all_photographers:
        if p.location and p.location not in photographer_locations:
            photographer_locations.append(p.location)

    return render_template(
        'customer/index.html',
        title='Home',
        photographers=photographers,
        featured_photographers=featured_photographers,
        service_categories=service_categories,
        photographer_locations=photographer_locations,
        page=page,
        total_pages=total_pages,
        total=total
    )


# Session-based basket routes removed - now using database cart only


@customer_bp.route('/bookings')
@login_required
def booking_history():
    user = get_current_user()

    customer = Customer.get_by_user_id(user.get('id'))
    if not customer:
        flash("Customer profile not found.")
        return redirect(url_for('customer.index'))

    bookings = Booking.get_by_customer_with_details(customer.id)

    return render_template(
        'customer/booking_history.html',
        title='My Bookings',
        bookings=bookings
    )

# View session packages for a photographer


@customer_bp.route('/session/<int:photographer_id>', methods=['GET'])
@login_required
@role_required('Customer')
def view_session(photographer_id):
    photographer = Photographer.get_by_id(photographer_id)
    packages = Package.get_by_photographer(photographer_id) if hasattr(
        Photographer, 'get_by_photographer') else []
    return render_template(
        'customer/session_package.html',
        title='Book a Session',
        photographer=photographer,
        packages=packages
    )

# cart operations


@customer_bp.route('/cart/add', methods=['POST'])
@login_required
@role_required('Customer')
def add_to_cart_db():
    package_id = request.form.get('package_id')
    photographer_id = request.form.get('photographer_id')
    user = get_current_user()
    customer = Customer.get_by_user_id(user.get('id'))

    if not (package_id and photographer_id and customer):
        flash('Invalid request.', 'error')
        return redirect(url_for('customer.index'))

    package = Package.get_by_id(package_id)
    price = package.price if package else 0.0
    cart = Cart.get_by_customer(customer.id, status='Pending')

    if not cart:
        cart = Cart.create(customer_id=customer.id, subtotal=0.0)

    CartItem.create(cart.id, photographer_id, package_id, price)
    Cart.update(cart.id, subtotal=cart.subtotal + price)

    flash('Item added to your cart.', 'success')
    return redirect(url_for('customer.view_cart'))


@customer_bp.route('/cart')
@login_required
@role_required('Customer')
def view_cart():
    """View customer's cart with database items"""
    user = get_current_user()
    customer = Customer.get_by_user_id(user.get('id'))
    
    if not customer:
        flash('Customer profile not found.', 'error')
        return redirect(url_for('customer.index'))
    
    cart = Cart.get_by_customer(customer.id)
    items = CartItem.get_by_cart(cart.id) if cart else []
    
    total = sum(float(item.price) for item in items)
    
    return render_template(
        'customer/cart.html',
        title='Your Cart',
        cart_items=items,
        total=total,
        cart=cart
    )

@customer_bp.route('/cart/remove', methods=['POST'])
@login_required
@role_required('Customer')
def remove_from_cart():
    """Remove item from cart"""
    cart_item_id = request.form.get('cart_item_id')
    user = get_current_user()
    customer = Customer.get_by_user_id(user.get('id'))
    
    if not cart_item_id or not customer:
        flash('Invalid request.', 'error')
        return redirect(url_for('customer.view_cart'))
    
    try:
        # Get cart item to verify ownership
        cart_item = CartItem.get_by_id(cart_item_id)
        if not cart_item:
            flash('Item not found.', 'error')
            return redirect(url_for('customer.view_cart'))
        
        # Get cart to verify it belongs to this customer
        cart = Cart.get_by_id(cart_item.cart_id)
        if not cart or cart.customer_id != customer.id:
            flash('You do not have permission to remove this item.', 'error')
            return redirect(url_for('customer.view_cart'))
        
        # Remove item and update cart total
        CartItem.delete(cart_item_id)
        Cart.update(cart.id, subtotal=cart.subtotal - cart_item.price)
        
        flash('Item removed from cart.', 'success')
    except Exception as e:
        flash(f'Error removing item: {str(e)}', 'error')
    
    return redirect(url_for('customer.view_cart'))


# ======== TEST ========


@customer_bp.route('/test_booking')
def test_booking():
    Booking.create(customer_id=1, photographer_id=1, package_id=1)
    return "Booking created successfully"


@customer_bp.route('/test_cart')
def test_cart():
    from project.models import Cart, CartItem
    customer_id = 1
    photographer_id = 1
    package_id = 1
    price = 350.0

    cart = Cart.get_by_customer(customer_id)
    if not cart:
        cart = Cart.create(customer_id=customer_id, subtotal=0.0)
    CartItem.create(cart.id, photographer_id, package_id, price)
    Cart.update(cart.id, subtotal=cart.subtotal + price)

    return f"Added package {package_id} to cart {cart.id}"


@customer_bp.route('/test_cart_update')
def test_cart_update():
    cart = Cart.get_by_customer(1)
    if not cart:
        return "No cart found"
    Cart.update(cart.id, subtotal=999.99)
    return f"Cart {cart.id} updated to subtotal 999.99"


@customer_bp.route('/test_cart_delete')
def test_cart_delete():
    cart = Cart.get_by_customer(1)
    if not cart:
        return "No cart found"
    Cart.delete(cart.id)
    return f"Cart {cart.id} deleted"


@customer_bp.route('/test_cartitem_delete')
def test_cartitem_delete():
    from project.models import CartItem
    items = CartItem.get_by_cart(1)
    if not items:
        return "No items in cart"
    CartItem.delete(items[0].id)
    return f"Deleted item {items[0].id}"


# ========= TEST END ========

# Submit a booking
@customer_bp.route('/book', methods=['POST'])
@login_required
@role_required('Customer')
def create_booking():
    package_id = request.form.get('package_id')
    photographer_id = request.form.get('photographer_id')
    user = get_current_user()
    customer = Customer.get_by_user_id(user.get('id'))

    if not (package_id and photographer_id and customer):
        flash('Invalid booking request.', 'error')
        return redirect(url_for('customer.index'))

    Booking.create(customer_id=customer.id,
                   photographer_id=photographer_id, package_id=package_id)
    flash('Your booking was successful!', 'success')
    return redirect(url_for('customer.success_page'))


@customer_bp.route('/checkout')
@login_required
@role_required('Customer')
def checkout():
    user = get_current_user()
    customer = Customer.get_by_user_id(user.get('id'))
    cart = Cart.get_by_customer(customer.id)
    items = CartItem.get_by_cart(cart.id) if cart else []

    cart_dict = {
        item.id: {
            'title': f'Package #{item.package_id}',
            'price': float(item.price),
            'qty': 1
        } for item in items
    }
    total = sum(i['price'] * i['qty'] for i in cart_dict.values())

    return render_template(
        'customer/checkout.html',      # << Checkout ची फाईल
        title='Checkout',
        cart=cart_dict,
        total=total
    )


@customer_bp.route('/success')
def success_page():
    return render_template('customer/success_page.html', title='Booking Success')


@customer_bp.route('/about')
def about():
    return render_template('customer/about.html', title='About')


@customer_bp.route('/contact')
def contact():
    return render_template('customer/contact.html', title='Contact')

# @customer_bp.route('/photographer/<int:photographer_id>/gallery')
# def photographer_gallery(photographer_id):
#     """Public gallery view for customers to view photographer's work"""
#     photographer = Photographer.get_by_id(photographer_id)

#     if not photographer:
#         flash('Photographer not found.', 'error')
#         return redirect(url_for('customer.index'))

#     # Get photographer's packages and portfolio items
#     packages = Package.get_by_photographer_id(photographer.id)
#     portfolioItems = PortfolioItem.get_by_photographer(photographer.id)

#     return render_template('customer/photographer_gallery.html',
#                          title=f'{photographer.user.full_name} - Gallery',
#                          photographer=photographer,
#                          packages=packages,
#                          portfolioItems=portfolioItems)


@photographer_bp.route('/dashboard')
@photographer_bp.route('/admin')
@role_required('Photographer')
def dashboard():
    """Photographer dashboard/admin page"""
    user = get_current_user()
    photographer = Photographer.get_by_user_id(user.get('id'))

    portfolioItems = PortfolioItem.get_by_photographer(photographer.id)
    packages = Package.get_by_photographer_id(photographer.id)

    # Initialize forms
    upload_form = PortfolioUploadForm()
    bio_form = PhotographerBioForm()
    package_form = SinglePackageForm()

    # Pre-populate bio form
    if photographer.bio:
        bio_form.bio.data = photographer.bio

    seen_category_ids = set()
    categories = []
    for package in packages:
        if package.category and package.category_id not in seen_category_ids:
            seen_category_ids.add(package.category_id)
            categories.append(package.category)

    return render_template('photographer/dashboard.html',
                           title='Photographer Dashboard',
                           portfolioItems=portfolioItems,
                           packages=packages,
                           photographer=photographer,
                           upload_form=upload_form,
                           bio_form=bio_form,
                           package_form=package_form,
                           categories=categories)


@photographer_bp.route('/create_package', methods=['POST'])
@role_required('Photographer')
def create_package():
    """Create a new package"""
    user = get_current_user()
    photographer = Photographer.get_by_user_id(user.get('id'))

    if not photographer:
        flash('Photographer profile not found.', 'error')
        return redirect(url_for('photographer.dashboard'))

    form = SinglePackageForm()

    if form.validate_on_submit():
        try:
            # Check if category is valid (not 0)
            if form.category.data == 0:
                flash('Please select a valid category.', 'error')
                return redirect(url_for('photographer.dashboard'))

            Package.create(
                package_name=form.package_name.data,
                photographer_id=photographer.id,
                category_id=form.category.data,
                price=form.price.data,
                inclusions=form.inclusions.data
            )
            flash('Package created successfully!', 'success')
        except Exception as e:
            flash(f'Error creating package: {str(e)}', 'error')
            import traceback
            print(traceback.format_exc())
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')

    return redirect(url_for('photographer.dashboard'))


@photographer_bp.route('/update_bio', methods=['POST'])
@role_required('Photographer')
def update_bio():
    """Update photographer bio/summary"""
    user = get_current_user()
    photographer = Photographer.get_by_user_id(user.get('id'))

    if not photographer:
        flash('Photographer profile not found.', 'error')
        return redirect(url_for('photographer.dashboard'))

    form = PhotographerBioForm()

    if form.validate_on_submit():
        try:
            Photographer.update(photographer.id, bio=form.bio.data)
            flash('Bio updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating bio: {str(e)}', 'error')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')

    return redirect(url_for('photographer.dashboard'))


@photographer_bp.route('/update_package/<int:package_id>', methods=['POST'])
@role_required('Photographer')
def update_package(package_id):
    """Update an existing package"""
    user = get_current_user()
    photographer = Photographer.get_by_user_id(user.get('id'))

    if not photographer:
        flash('Photographer profile not found.', 'error')
        return redirect(url_for('photographer.dashboard'))

    package = Package.get_by_id(package_id)

    if not package:
        flash('Package not found.', 'error')
        return redirect(url_for('photographer.dashboard'))

    # Verify ownership
    if package.photographer_id != photographer.id:
        flash('You do not have permission to edit this package.', 'error')
        return redirect(url_for('photographer.dashboard'))

    try:
        package_name = request.form.get('package_name')
        category_id = int(request.form.get('category'))
        price = float(request.form.get('price'))
        inclusions = request.form.get('inclusions')

        # Validate inputs
        if not all([package_name, category_id, price, inclusions]):
            flash('All fields are required.', 'error')
            return redirect(url_for('photographer.dashboard'))

        if category_id == 0:
            flash('Please select a valid category.', 'error')
            return redirect(url_for('photographer.dashboard'))

        Package.update(
            package_id,
            package_name=package_name,
            category_id=category_id,
            price=price,
            inclusions=inclusions
        )
        flash('Package updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating package: {str(e)}', 'error')
        import traceback
        print(traceback.format_exc())

    return redirect(url_for('photographer.dashboard'))


@photographer_bp.route('/delete_package/<int:package_id>', methods=['POST'])
@role_required('Photographer')
def delete_package(package_id):
    """Delete a package"""
    user = get_current_user()
    photographer = Photographer.get_by_user_id(user.get('id'))

    if not photographer:
        flash('Photographer profile not found.', 'error')
        return redirect(url_for('photographer.dashboard'))

    try:
        package = Package.get_by_id(package_id)

        if not package:
            flash('Package not found.', 'error')
            return redirect(url_for('photographer.dashboard'))

        # Verify ownership
        if package.photographer_id != photographer.id:
            flash('You do not have permission to delete this package.', 'error')
            return redirect(url_for('photographer.dashboard'))

        Package.delete(package_id)
        flash('Package deleted successfully!', 'success')

    except Exception as e:
        flash(f'Error deleting package: {str(e)}', 'error')

    return redirect(url_for('photographer.dashboard'))


@photographer_bp.route('/upload_portfolio', methods=['POST'])
@role_required('Photographer')
def upload_portfolio():
    """Handle portfolio image upload using WTForms"""
    user = get_current_user()
    photographer = Photographer.get_by_user_id(user.get('id'))

    if not photographer:
        flash('Photographer profile not found.', 'error')
        return redirect(url_for('photographer.dashboard'))

    form = PortfolioUploadForm()

    if form.validate_on_submit():
        try:
            file = form.portfolio_image.data
            title = form.title.data
            caption = form.caption.data

            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)

            if file_size > MAX_FILE_SIZE:
                flash('File size exceeds 50MB limit.', 'error')
                return redirect(url_for('photographer.dashboard'))

            # Secure the filename
            filename = secure_filename(file.filename)

            # Create unique filename to avoid conflicts
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name, ext = os.path.splitext(filename)
            unique_filename = f"{photographer.id}_{timestamp}_{name}{ext}"

            # Get upload path - use constant or app config
            upload_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)

            # Ensure upload directory exists
            os.makedirs(upload_path, exist_ok=True)

            # Save file
            file_path = os.path.join(upload_path, unique_filename)
            file.save(file_path)

            # Create portfolio item in database
            PortfolioItem.create(
                photographer_id=photographer.id,
                title=title,
                image_path=unique_filename,
                caption=caption if caption else None
            )

            flash('Portfolio item uploaded successfully!', 'success')

        except Exception as e:
            flash(f'Error uploading file: {str(e)}', 'error')
            import traceback
            print(traceback.format_exc())
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')

    return redirect(url_for('photographer.dashboard'))


@photographer_bp.route('/delete_portfolio/<int:portfolio_id>', methods=['POST'])
@role_required('Photographer')
def delete_portfolio(portfolio_id):
    """Delete a portfolio item"""
    user = get_current_user()
    photographer = Photographer.get_by_user_id(user.get('id'))

    if not photographer:
        flash('Photographer profile not found.', 'error')
        return redirect(url_for('photographer.dashboard'))

    try:
        portfolio_item = PortfolioItem.get_by_id(portfolio_id)

        if not portfolio_item:
            flash('Portfolio item not found.', 'error')
            return redirect(url_for('photographer.dashboard'))

        # Verify ownership
        if portfolio_item.photographer_id != photographer.id:
            flash('You do not have permission to delete this item.', 'error')
            return redirect(url_for('photographer.dashboard'))

        # Get upload path
        upload_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)

        # Delete file from filesystem
        file_path = os.path.join(upload_path, portfolio_item.image_path)
        if os.path.exists(file_path):
            os.remove(file_path)

        # Delete from database
        PortfolioItem.delete(portfolio_id)

        flash('Portfolio item deleted successfully!', 'success')

    except Exception as e:
        flash(f'Error deleting portfolio item: {str(e)}', 'error')
        import traceback
        print(traceback.format_exc())

    return redirect(url_for('photographer.dashboard'))


@photographer_bp.route('/gallery')
@photographer_bp.route('/gallery/<int:photographer_id>')
def gallery(photographer_id=None):
    if photographer_id:
        photographer = Photographer.get_by_id(photographer_id)
    else:
        # Default to first photographer if no ID provided
        photographers = Photographer.get_all()
        photographer = photographers[0] if photographers else None

    if not photographer:
        flash('Photographer not found.', 'error')
        return redirect(url_for('customer.index'))

    # Get photographer's packages
    packages = Package.get_by_photographer_id(photographer.id)

    # Extract unique categories from packages
    seen_category_ids = set()
    categories = []
    for package in packages:
        if package.category and package.category_id not in seen_category_ids:
            seen_category_ids.add(package.category_id)
            categories.append(package.category)

    # Get portfolio items
    portfolioItems = PortfolioItem.get_by_photographer(photographer.id)

    return render_template(
        'photographer/gallery.html',
        title='Gallery',
        photographer=photographer,
        categories=categories,
        portfolioItems=portfolioItems
    )


@customer_bp.route('/session-package/<int:photographer_id>')
def session_package(photographer_id):
    photographer = Photographer.get_by_id(photographer_id)
    if not photographer:
        flash('Photographer not found.', 'error')
        return redirect(url_for('customer.index'))

    # Get category_id from query parameter
    category_id = request.args.get('category_id', type=int)

    if category_id:
        # Filter packages by photographer AND category
        all_packages = Package.get_by_photographer_id(photographer_id)
        packages = [
            pkg for pkg in all_packages if pkg.category_id == category_id]

        # Get category for display
        category = Category.get_by_id(category_id)
    else:
        # If no category specified, show all packages
        packages = Package.get_by_photographer_id(photographer_id)
        category = None

    return render_template(
        'customer/session_package.html',
        title='Book Session',
        photographer=photographer,
        packages=packages,
        category=category,
        today_date=datetime.now().date().isoformat()
    )


@admin_bp.route('/', methods=['GET', 'POST'])
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if is_authenticated():
        user = get_current_user()
        if user and user.get('role') == 'Admin':
            return redirect(url_for('admin.dashboard'))
        if user and user.get('role') == 'Photographer':
            return redirect(url_for('photographer.dashboard'))
        if user and user.get('role') == 'Customer':
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
    users_with_roles = [{'user': u, 'role': u.role} for u in all_users]
    return render_template('admin/users.html', title='Manage Users', users=users_with_roles)

@admin_bp.route('/bookings')
@role_required('Admin')
def bookings():
    all_bookings = Booking.get_all()
    return render_template('admin/bookings.html', title='All Bookings', bookings=all_bookings)
