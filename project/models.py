from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import fetch_one, fetch_all, execute_query

class User:
    """User model for authentication and user management."""

    def __init__(self, user_dict):
        if user_dict:
            self.id = user_dict.get('id')
            self.email = user_dict.get('email')
            self.password_hash = user_dict.get('password_hash')
            self.first_name = user_dict.get('first_name')
            self.last_name = user_dict.get('last_name')
            self.role = user_dict.get('role')
            self.profile_image = user_dict.get('profile_image')
            self.phone = user_dict.get('phone')
            self.created_at = user_dict.get('created_at')
            self.updated_at = user_dict.get('updated_at')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def set_password(self, password):
        return generate_password_hash(password, method='pbkdf2:sha256')

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

    @staticmethod
    def get_by_id(user_id):
        user_data = fetch_one("SELECT * FROM users WHERE id = %s", (user_id,))
        return User(user_data) if user_data else None

    @staticmethod
    def get_by_email(email):
        user_data = fetch_one("SELECT * FROM users WHERE email = %s", (email,))
        return User(user_data) if user_data else None

    @staticmethod
    def get_all():
        users_data = fetch_all("SELECT * FROM users")
        return [User(user) for user in users_data]

    @staticmethod
    def get_by_role(role):
        """Get all users with a specific role (Customer, Photographer, Admin)."""
        users_data = fetch_all("SELECT * FROM users WHERE role = %s", (role,))
        return [User(user) for user in users_data]

    @staticmethod
    def create(email, password, first_name, last_name, role, phone=None, profile_image=None):
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        user_id = execute_query(
            """
            INSERT INTO users (email, password_hash, first_name, last_name,
                              role, phone, profile_image, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (email, password_hash, first_name, last_name, role, phone,
             profile_image, datetime.utcnow())
        )
        return User.get_by_id(user_id)

    @staticmethod
    def update(user_id, **kwargs):
        allowed_fields = ['email', 'first_name', 'last_name', 'role', 'phone', 'profile_image']
        updates = []
        values = []

        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = %s")
                values.append(value)

        if updates:
            values.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
            execute_query(query, tuple(values))

        return User.get_by_id(user_id)

    @staticmethod
    def update_password(user_id, new_password):
        password_hash = generate_password_hash(new_password, method='pbkdf2:sha256')
        execute_query(
            "UPDATE users SET password_hash = %s WHERE id = %s",
            (password_hash, user_id)
        )

    @staticmethod
    def delete(user_id):
        execute_query("DELETE FROM users WHERE id = %s", (user_id,))

    def __repr__(self):
        return f'<User {self.email}>'


class Customer:
    """Customer profile model."""

    def __init__(self, customer_dict):
        if customer_dict:
            self.id = customer_dict.get('id')
            self.user_id = customer_dict.get('user_id')
            self.address = customer_dict.get('address')
            self.city = customer_dict.get('city')
            self.postcode = customer_dict.get('postcode')
            self.billing_address = customer_dict.get('billing_address')

            if 'user_first_name' in customer_dict:
                self.user = type('User', (), {
                    'id': customer_dict.get('user_id'),
                    'first_name': customer_dict.get('user_first_name'),
                    'last_name': customer_dict.get('user_last_name'),
                    'email': customer_dict.get('user_email'),
                    'phone': customer_dict.get('user_phone'),
                    'profile_image': customer_dict.get('user_profile_image'),
                    'full_name': f"{customer_dict.get('user_first_name')} {customer_dict.get('user_last_name')}"
                })()
            else:
                self.user = None

    @staticmethod
    def get_by_id(customer_id):
        customer_data = fetch_one(
            """
            SELECT c.*,
                   u.first_name as user_first_name,
                   u.last_name as user_last_name,
                   u.email as user_email,
                   u.phone as user_phone,
                   u.profile_image as user_profile_image
            FROM customers c
            JOIN users u ON c.user_id = u.id
            WHERE c.id = %s
            """,
            (customer_id,)
        )
        return Customer(customer_data) if customer_data else None

    @staticmethod
    def get_by_user_id(user_id):
        customer_data = fetch_one(
            """
            SELECT c.*,
                   u.first_name as user_first_name,
                   u.last_name as user_last_name,
                   u.email as user_email,
                   u.phone as user_phone,
                   u.profile_image as user_profile_image
            FROM customers c
            JOIN users u ON c.user_id = u.id
            WHERE c.user_id = %s
            """,
            (user_id,)
        )
        return Customer(customer_data) if customer_data else None

    @staticmethod
    def get_all():
        customers_data = fetch_all(
            """
            SELECT c.*,
                   u.first_name as user_first_name,
                   u.last_name as user_last_name,
                   u.email as user_email,
                   u.phone as user_phone,
                   u.profile_image as user_profile_image
            FROM customers c
            JOIN users u ON c.user_id = u.id
            """
        )
        return [Customer(c) for c in customers_data]

    @staticmethod
    def create(user_id, postcode, address=None, city=None, billing_address=None):
        customer_id = execute_query(
            """
            INSERT INTO customers (user_id, address, city, postcode, billing_address)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, address, city, postcode, billing_address)
        )
        return Customer.get_by_id(customer_id)

    @staticmethod
    def update(customer_id, **kwargs):
        allowed_fields = ['address', 'city', 'postcode', 'billing_address']
        updates = []
        values = []

        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = %s")
                values.append(value)

        if updates:
            values.append(customer_id)
            query = f"UPDATE customers SET {', '.join(updates)} WHERE id = %s"
            execute_query(query, tuple(values))

        return Customer.get_by_id(customer_id)

    @staticmethod
    def delete(customer_id):
        execute_query("DELETE FROM customers WHERE id = %s", (customer_id,))

    def __repr__(self):
        return f'<Customer {self.id}>'


class Category:
    """Category model for grouping photographer services."""

    def __init__(self, category_dict):
        if category_dict:
            self.id = category_dict.get('id')
            self.category_name = category_dict.get('category_name')
            self.description = category_dict.get('description')

    @staticmethod
    def get_by_id(category_id):
        category_data = fetch_one(
            "SELECT * FROM category WHERE id = %s",
            (category_id,)
        )
        return Category(category_data) if category_data else None

    @staticmethod
    def get_by_name(category_name):
        category_data = fetch_one(
            "SELECT * FROM category WHERE category_name = %s",
            (category_name,)
        )
        return Category(category_data) if category_data else None

    @staticmethod
    def get_all():
        categories_data = fetch_all("SELECT * FROM category")
        return [Category(c) for c in categories_data]

    @staticmethod
    def create(category_name, description=None):
        category_id = execute_query(
            "INSERT INTO category (category_name, description) VALUES (%s, %s)",
            (category_name, description)
        )
        return Category.get_by_id(category_id)

    @staticmethod
    def update(category_id, **kwargs):
        allowed_fields = ['category_name', 'description']
        updates = []
        values = []

        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = %s")
                values.append(value)

        if updates:
            values.append(category_id)
            query = f"UPDATE category SET {', '.join(updates)} WHERE id = %s"
            execute_query(query, tuple(values))

        return Category.get_by_id(category_id)

    @staticmethod
    def delete(category_id):
        execute_query("DELETE FROM category WHERE id = %s", (category_id,))

    def __repr__(self):
        return f'<Category {self.category_name}>'


class Package:
    """Package model for photography service packages."""

    def __init__(self, package_dict):
        if package_dict:
            self.id = package_dict.get('id')
            self.package_name = package_dict.get('package_name')
            self.photographer_id = package_dict.get('photographer_id')
            self.category_id = package_dict.get('category_id')
            self.price = package_dict.get('price')
            self.inclusions = package_dict.get('inclusions')
            
            # Adding category information if available
            if 'category_name' in package_dict:
                self.category = type('Category', (), {
                    'id': package_dict.get('category_id'),
                    'category_name': package_dict.get('category_name'),
                    'description': package_dict.get('category_description')
                })()
            else:
                self.category = None

    @staticmethod
    def get_by_id(package_id):
        package_data = fetch_one(
            """
            SELECT p.*, c.category_name, c.description as category_description
            FROM packages p
            LEFT JOIN category c ON p.category_id = c.id
            WHERE p.id = %s
            """,
            (package_id,)
        )
        return Package(package_data) if package_data else None

    @staticmethod
    def get_by_name(package_name):
        package_data = fetch_one(
            """
            SELECT p.*, c.category_name, c.description as category_description
            FROM packages p
            LEFT JOIN category c ON p.category_id = c.id
            WHERE p.package_name = %s
            """,
            (package_name,)
        )
        return Package(package_data) if package_data else None

    @staticmethod
    def get_all():
        packages_data = fetch_all(
            """
            SELECT p.*, c.category_name, c.description as category_description
            FROM packages p
            LEFT JOIN category c ON p.category_id = c.id
            """
        )
        return [Package(p) for p in packages_data]
    
    @staticmethod
    def get_by_photographer_id(photographer_id):
        package_data = fetch_all(
            """
            SELECT p.*, c.category_name, c.description as category_description
            FROM packages p
            LEFT JOIN category c ON p.category_id = c.id
            WHERE p.photographer_id = %s
            ORDER BY 
                CASE p.package_name
                    WHEN 'Basic' THEN 1
                    WHEN 'Standard' THEN 2
                    WHEN 'Premium' THEN 3
                END
            """,
            (photographer_id,)
        )
        return [Package(p) for p in package_data]

    @staticmethod
    def get_by_category(category_id):
        """Get all packages for a specific category"""
        package_data = fetch_all(
            """
            SELECT p.*, c.category_name, c.description as category_description
            FROM packages p
            LEFT JOIN category c ON p.category_id = c.id
            WHERE p.category_id = %s
            """,
            (category_id,)
        )
        return [Package(p) for p in package_data]

    @staticmethod
    def create(package_name, photographer_id, category_id, price, inclusions):
        """Create a new package with category_id"""
        package_id = execute_query(
            """
            INSERT INTO packages (package_name, photographer_id, category_id, price, inclusions) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (package_name, photographer_id, category_id, price, inclusions)
        )
        return Package.get_by_id(package_id)

    @staticmethod
    def update(package_id, **kwargs):
        allowed_fields = ['package_name', 'category_id', 'price', 'inclusions']
        updates = []
        values = []

        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = %s")
                values.append(value)

        if updates:
            values.append(package_id)
            query = f"UPDATE packages SET {', '.join(updates)} WHERE id = %s"
            execute_query(query, tuple(values))

        return Package.get_by_id(package_id)

    @staticmethod
    def delete(package_id):
        execute_query("DELETE FROM packages WHERE id = %s", (package_id,))

    def __repr__(self):
        return f'<Package {self.package_name}>'

class Photographer:
    """Photographer profile model."""

    def __init__(self, photographer_dict):
        if photographer_dict:
            self.id = photographer_dict.get('id')
            self.user_id = photographer_dict.get('user_id')
            self.category_id = photographer_dict.get('category_id')
            self.bio = photographer_dict.get('bio')
            self.location = photographer_dict.get('location')
            self.social_link = photographer_dict.get('social_link')
            self.availability = photographer_dict.get('availability')
            self.featured = photographer_dict.get('featured', False)

            if 'user_first_name' in photographer_dict:
                self.user = type('User', (), {
                    'id': photographer_dict.get('user_id'),
                    'first_name': photographer_dict.get('user_first_name'),
                    'last_name': photographer_dict.get('user_last_name'),
                    'email': photographer_dict.get('user_email'),
                    'phone': photographer_dict.get('user_phone'),
                    'profile_image': photographer_dict.get('user_profile_image'),
                    'full_name': f"{photographer_dict.get('user_first_name')} {photographer_dict.get('user_last_name')}"
                })()
            else:
                self.user = None

            if 'category_name' in photographer_dict:
                self.category = type('Category', (), {
                    'id': photographer_dict.get('category_id'),
                    'category_name': photographer_dict.get('category_name'),
                    'description': photographer_dict.get('category_description')
                })()
            else:
                self.category = None

    @staticmethod
    def get_by_id(photographer_id):
        photographer_data = fetch_one(
            """
            SELECT p.*,
                   u.first_name as user_first_name,
                   u.last_name as user_last_name,
                   u.email as user_email,
                   u.phone as user_phone,
                   u.profile_image as user_profile_image,
                   c.category_name as category_name,
                   c.description as category_description
            FROM photographers p
            JOIN users u ON p.user_id = u.id
            LEFT JOIN category c ON p.category_id = c.id
            WHERE p.id = %s
            """,
            (photographer_id,)
        )
        return Photographer(photographer_data) if photographer_data else None

    @staticmethod
    def get_by_user_id(user_id):
        photographer_data = fetch_one(
            """
            SELECT p.*,
                   u.first_name as user_first_name,
                   u.last_name as user_last_name,
                   u.email as user_email,
                   u.phone as user_phone,
                   u.profile_image as user_profile_image,
                   c.category_name as category_name,
                   c.description as category_description
            FROM photographers p
            JOIN users u ON p.user_id = u.id
            LEFT JOIN category c ON p.category_id = c.id
            WHERE p.user_id = %s
            """,
            (user_id,)
        )
        return Photographer(photographer_data) if photographer_data else None

    @staticmethod
    def get_all():
        photographers_data = fetch_all(
            """
            SELECT p.*,
                   u.first_name as user_first_name,
                   u.last_name as user_last_name,
                   u.email as user_email,
                   u.phone as user_phone,
                   u.profile_image as user_profile_image,
                   c.category_name as category_name,
                   c.description as category_description
            FROM photographers p
            JOIN users u ON p.user_id = u.id
            LEFT JOIN category c ON p.category_id = c.id
            """
        )
        return [Photographer(p) for p in photographers_data]

    @staticmethod
    def get_by_category(category_id):
        photographers_data = fetch_all(
            """
            SELECT p.*,
                   u.first_name as user_first_name,
                   u.last_name as user_last_name,
                   u.email as user_email,
                   u.phone as user_phone,
                   u.profile_image as user_profile_image,
                   c.category_name as category_name,
                   c.description as category_description
            FROM photographers p
            JOIN users u ON p.user_id = u.id
            LEFT JOIN category c ON p.category_id = c.id
            WHERE p.category_id = %s
            """,
            (category_id,)
        )
        return [Photographer(p) for p in photographers_data]

    @staticmethod
    def get_featured():
        """Get featured photographers."""
        photographers_data = fetch_all(
            """
            SELECT p.*,
                   u.first_name as user_first_name,
                   u.last_name as user_last_name,
                   u.email as user_email,
                   u.phone as user_phone,
                   u.profile_image as user_profile_image,
                   c.category_name as category_name,
                   c.description as category_description
            FROM photographers p
            JOIN users u ON p.user_id = u.id
            LEFT JOIN category c ON p.category_id = c.id
            WHERE p.featured = TRUE
            LIMIT 3
            """
        )
        return [Photographer(p) for p in photographers_data]

    @staticmethod
    def create(user_id, category_id, location, social_link, availability, bio=None):
        photographer_id = execute_query(
            """
            INSERT INTO photographers (user_id, category_id, bio, location, social_link, availability)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, category_id, bio, location, social_link, availability)
        )
        return Photographer.get_by_id(photographer_id)

    @staticmethod
    def update(photographer_id, **kwargs):
        allowed_fields = ['category_id', 'bio', 'location', 'social_link', 'availability', 'featured']
        updates = []
        values = []

        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = %s")
                values.append(value)

        if updates:
            values.append(photographer_id)
            query = f"UPDATE photographers SET {', '.join(updates)} WHERE id = %s"
            execute_query(query, tuple(values))

        return Photographer.get_by_id(photographer_id)

    @staticmethod
    def toggle_featured(photographer_id):
        """Toggle featured status for a photographer."""
        execute_query(
            "UPDATE photographers SET featured = NOT featured WHERE id = %s",
            (photographer_id,)
        )
        return Photographer.get_by_id(photographer_id)

    @staticmethod
    def delete(photographer_id):
        execute_query("DELETE FROM photographers WHERE id = %s",
                      (photographer_id,))

    def __repr__(self):
        return f'<Photographer {self.id}>'


class PortfolioItem:
    """Portfolio item model for photographer portfolios."""

    def __init__(self, portfolio_dict):
        if portfolio_dict:
            self.id = portfolio_dict.get('id')
            self.photographer_id = portfolio_dict.get('photographer_id')
            self.title = portfolio_dict.get('title')
            self.caption = portfolio_dict.get('caption')
            self.image_path = portfolio_dict.get('image_path')
            self.created_at = portfolio_dict.get('created_at')

    @staticmethod
    def get_by_id(portfolio_id):
        portfolio_data = fetch_one(
            "SELECT * FROM portfolio_items WHERE id = %s",
            (portfolio_id,)
        )
        return PortfolioItem(portfolio_data) if portfolio_data else None

    @staticmethod
    def get_by_photographer(photographer_id):
        portfolio_data = fetch_all(
            "SELECT * FROM portfolio_items WHERE photographer_id = %s ORDER BY created_at DESC",
            (photographer_id,)
        )
        return [PortfolioItem(p) for p in portfolio_data]

    @staticmethod
    def get_all():
        portfolio_data = fetch_all(
            "SELECT * FROM portfolio_items ORDER BY created_at DESC")
        return [PortfolioItem(p) for p in portfolio_data]

    @staticmethod
    def create(photographer_id, title, image_path, caption=None):
        portfolio_id = execute_query(
            """
            INSERT INTO portfolio_items (photographer_id, title, caption, image_path, created_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (photographer_id, title, caption, image_path, datetime.now())
        )
        return PortfolioItem.get_by_id(portfolio_id)

    @staticmethod
    def update(portfolio_id, title=None, caption=None, image_path=None):
        allowed_fields = {'title': title,
                          'caption': caption, 'image_path': image_path}
        updates = []
        values = []

        for field, value in allowed_fields.items():
            if value is not None:
                updates.append(f"{field} = %s")
                values.append(value)

        if updates:
            values.append(portfolio_id)
            query = f"UPDATE portfolio_items SET {', '.join(updates)} WHERE id = %s"
            execute_query(query, tuple(values))

        return PortfolioItem.get_by_id(portfolio_id)

    @staticmethod
    def delete(portfolio_id):
        execute_query(
            "DELETE FROM portfolio_items WHERE id = %s", (portfolio_id,))

    def __repr__(self):
        return f'<PortfolioItem {self.title}>'


class Cart:
    """Cart model for customer shopping cart."""

    def __init__(self, cart_dict):
        if cart_dict:
            self.id = cart_dict.get('id')
            self.customer_id = cart_dict.get('customer_id')
            self.subtotal = cart_dict.get('subtotal')
            self.status = cart_dict.get('status')
            self.created_at = cart_dict.get('created_at')

    @staticmethod
    def get_by_id(cart_id):
        cart_data = fetch_one(
            "SELECT * FROM cart WHERE id = %s",
            (cart_id,)
        )
        return Cart(cart_data) if cart_data else None

    @staticmethod
    def get_by_customer(customer_id, status='Pending'):
        """Get customer's cart by status (default: Pending)."""
        cart_data = fetch_one(
            "SELECT * FROM cart WHERE customer_id = %s AND status = %s ORDER BY created_at DESC",
            (customer_id, status)
        )
        return Cart(cart_data) if cart_data else None

    @staticmethod
    def get_all_by_customer(customer_id):
        """Get all carts for a customer."""
        carts_data = fetch_all(
            "SELECT * FROM cart WHERE customer_id = %s ORDER BY created_at DESC",
            (customer_id,)
        )
        return [Cart(c) for c in carts_data]

    @staticmethod
    def create(customer_id, subtotal=0.0, status='Pending'):
        cart_id = execute_query(
            "INSERT INTO cart (customer_id, subtotal, status, created_at) VALUES (%s, %s, %s, %s)",
            (customer_id, subtotal, status, datetime.utcnow())
        )
        return Cart.get_by_id(cart_id)

    @staticmethod
    def update(cart_id, **kwargs):
        allowed_fields = ['subtotal', 'status']
        updates = []
        values = []

        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = %s")
                values.append(value)

        if updates:
            values.append(cart_id)
            query = f"UPDATE cart SET {', '.join(updates)} WHERE id = %s"
            execute_query(query, tuple(values))

        return Cart.get_by_id(cart_id)

    @staticmethod
    def delete(cart_id):
        execute_query("DELETE FROM cart WHERE id = %s", (cart_id,))

    def __repr__(self):
        return f'<Cart {self.id}>'


class CartItem:
    """Cart item model for items in customer shopping cart."""

    def __init__(self, cart_item_dict):
        if cart_item_dict:
            self.id = cart_item_dict.get('id')
            self.cart_id = cart_item_dict.get('cart_id')
            self.photographer_id = cart_item_dict.get('photographer_id')
            self.package_id = cart_item_dict.get('package_id')
            self.price = cart_item_dict.get('price')
            self.event_date = cart_item_dict.get('event_date')
            self.event_time = cart_item_dict.get('event_time')
            self.pax = cart_item_dict.get('pax')
            self.notes = cart_item_dict.get('notes')
            self.created_at = cart_item_dict.get('created_at')
            
            # Additional fields from JOIN queries
            self.package_name = cart_item_dict.get('package_name')
            self.inclusions = cart_item_dict.get('inclusions')
            self.photographer_location = cart_item_dict.get('photographer_location')
            self.photographer_first_name = cart_item_dict.get('photographer_first_name')
            self.photographer_last_name = cart_item_dict.get('photographer_last_name')

    @staticmethod
    def get_by_id(cart_item_id):
        cart_item_data = fetch_one(
            "SELECT * FROM cart_item WHERE id = %s",
            (cart_item_id,)
        )
        return CartItem(cart_item_data) if cart_item_data else None

    @staticmethod
    def get_by_cart(cart_id):
        """Get all items in a cart."""
        cart_items_data = fetch_all(
            """
            SELECT ci.*,
                   p.package_name,
                   p.inclusions,
                   ph.location as photographer_location,
                   u.first_name as photographer_first_name,
                   u.last_name as photographer_last_name
            FROM cart_item ci
            JOIN packages p ON ci.package_id = p.id
            JOIN photographers ph ON ci.photographer_id = ph.id
            JOIN users u ON ph.user_id = u.id
            WHERE ci.cart_id = %s
            """,
            (cart_id,)
        )
        return [CartItem(ci) for ci in cart_items_data]

    @staticmethod
    def create(cart_id, photographer_id, package_id, price, event_date=None, event_time=None, pax=None, notes=None):
        cart_item_id = execute_query(
            "INSERT INTO cart_item (cart_id, photographer_id, package_id, price, event_date, event_time, pax, notes, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (cart_id, photographer_id, package_id, price, event_date, event_time, pax, notes, datetime.utcnow())
        )
        return CartItem.get_by_id(cart_item_id)

    @staticmethod
    def update(cart_item_id, **kwargs):
        allowed_fields = ['photographer_id', 'package_id', 'price']
        updates = []
        values = []

        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = %s")
                values.append(value)

        if updates:
            values.append(cart_item_id)
            query = f"UPDATE cart_item SET {', '.join(updates)} WHERE id = %s"
            execute_query(query, tuple(values))

        return CartItem.get_by_id(cart_item_id)

    @staticmethod
    def delete(cart_item_id):
        execute_query("DELETE FROM cart_item WHERE id = %s", (cart_item_id,))

    def __repr__(self):
        return f'<CartItem {self.id}>'


class Booking:
    """Booking model for customer bookings."""

    def __init__(self, booking_dict):
        if booking_dict:
            self.id = booking_dict.get('id')
            self.cart_id = booking_dict.get('cart_id')
            self.customer_id = booking_dict.get('customer_id')
            self.created_at = booking_dict.get('created_at')
            self.updated_at = booking_dict.get('updated_at')
            self.payment_date = booking_dict.get('payment_date')
            self.total_amount = booking_dict.get('total_amount')
            self.status = booking_dict.get('status')
            self.cart_items = []
            self.photographer_name = booking_dict.get('photographer_name')
            self.package_name = booking_dict.get('package_name')
            self.package_inclusions = booking_dict.get('package_inclusions')

    @staticmethod
    def get_by_id(booking_id):
        booking_data = fetch_one(
            "SELECT * FROM bookings WHERE id = %s",
            (booking_id,)
        )
        return Booking(booking_data) if booking_data else None
    
    @staticmethod
    def get_by_customer_with_details(customer_id):
        """Gets all bookings for a customer with related cart items and photographer details."""
        bookings_data = fetch_all(
            """
            SELECT DISTINCT
                b.id,
                b.cart_id,
                b.customer_id,
                b.created_at,
                b.updated_at,
                b.payment_date,
                b.total_amount,
                b.status,
                GROUP_CONCAT(DISTINCT CONCAT(u.first_name, ' ', u.last_name) SEPARATOR ', ') as photographer_name,
                GROUP_CONCAT(DISTINCT pkg.package_name SEPARATOR ', ') as package_name,
                GROUP_CONCAT(DISTINCT pkg.inclusions SEPARATOR '; ') as package_inclusions
            FROM bookings b
            LEFT JOIN cart c ON c.id = b.cart_id
            LEFT JOIN cart_item ci ON ci.cart_id = c.id
            LEFT JOIN photographers ph ON ph.id = ci.photographer_id
            LEFT JOIN users u ON u.id = ph.user_id
            LEFT JOIN packages pkg ON pkg.id = ci.package_id
            WHERE b.customer_id = %s
            GROUP BY b.id, b.cart_id, b.customer_id, b.created_at, b.updated_at, 
                     b.payment_date, b.total_amount, b.status
            ORDER BY b.created_at DESC
            """,
            (customer_id,)
        )
        return [Booking(b) for b in bookings_data]
    
    
    @staticmethod
    def get_by_customer(customer_id):
        bookings_data = fetch_all(
            "SELECT * FROM bookings WHERE customer_id = %s ORDER BY created_at DESC",
            (customer_id,)
        )
        return [Booking(b) for b in bookings_data]

    @staticmethod
    def get_by_cart(cart_id):
        booking_data = fetch_one(
            "SELECT * FROM bookings WHERE cart_id = %s",
            (cart_id,)
        )
        return Booking(booking_data) if booking_data else None

    @staticmethod
    def get_all():
        bookings_data = fetch_all("SELECT * FROM bookings ORDER BY created_at DESC")
        return [Booking(b) for b in bookings_data]

    @staticmethod
    def create(customer_id, photographer_id, package_id):
        cart_id = execute_query(
            "INSERT INTO cart (customer_id, subtotal, created_at) VALUES (%s, %s, %s)",
            (customer_id, 0.0, datetime.utcnow())
        )

        package = fetch_one("SELECT price FROM packages WHERE id = %s", (package_id,))
        price = package['price'] if package else 0.0

        execute_query(
            """
            INSERT INTO cart_item (cart_id, photographer_id, package_id, price, created_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (cart_id, photographer_id, package_id, price, datetime.utcnow())
        )

        booking_id = execute_query(
            """
            INSERT INTO bookings (cart_id, customer_id, total_amount, status, created_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (cart_id, customer_id, price, 'Pending', datetime.utcnow())
        )
        Cart.update(cart_id, subtotal=price, status='Completed')

        return Booking.get_by_id(booking_id)

    @staticmethod
    def update(booking_id, **kwargs):
        allowed_fields = ['total_amount', 'status', 'payment_date']
        updates = []
        values = []

        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = %s")
                values.append(value)

        if updates:
            values.append(booking_id)
            query = f"UPDATE bookings SET {', '.join(updates)} WHERE id = %s"
            execute_query(query, tuple(values))

        return Booking.get_by_id(booking_id)

    @staticmethod
    def update_status(booking_id, status, payment_date=None):
        if payment_date:
            execute_query(
                "UPDATE bookings SET status = %s, payment_date = %s WHERE id = %s",
                (status, payment_date, booking_id)
            )
        else:
            execute_query(
                "UPDATE bookings SET status = %s WHERE id = %s",
                (status, booking_id)
            )
        return Booking.get_by_id(booking_id)

    @staticmethod
    def delete(booking_id):
        execute_query("DELETE FROM bookings WHERE id = %s", (booking_id,))

    @staticmethod
    def create_from_cart(cart_id, customer_id, total_amount):
        """Create booking from existing cart without clearing cart items"""
        from database import execute_query
        
        # Create booking record
        booking_id = execute_query(
            """
            INSERT INTO bookings (cart_id, customer_id, total_amount, status, payment_date, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (cart_id, customer_id, total_amount, 'Completed', datetime.utcnow(), datetime.utcnow())
        )
        
        # Update cart status to Completed (preserve cart and cart_item records)
        Cart.update(cart_id, status='Completed')
        
        return booking_id

    def __repr__(self):
        return f'<Booking {self.id}>'
    
    
