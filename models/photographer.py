from datetime import datetime
from ..database import fetch_one, fetch_all, execute_query


class Photographer:
    """Photographer profile model."""

    def __init__(self, photographer_dict):
        """Initialize photographer from database dictionary."""
        if photographer_dict:
            self.id = photographer_dict.get('id')
            self.user_id = photographer_dict.get('user_id')
            self.bio = photographer_dict.get('bio')
            self.phone = photographer_dict.get('phone')
            self.location = photographer_dict.get('location')
            self.social_link = photographer_dict.get('social_link')
            self.created_at = photographer_dict.get('created_at')

            # Create user object if user data is present
            if 'user_first_name' in photographer_dict:
                self.user = type('User', (), {
                    'id': photographer_dict.get('user_id'),
                    'first_name': photographer_dict.get('user_first_name'),
                    'last_name': photographer_dict.get('user_last_name'),
                    'email': photographer_dict.get('user_email'),
                    'profile_image': photographer_dict.get('user_profile_image'),
                    'full_name': f"{photographer_dict.get('user_first_name')} {photographer_dict.get('user_last_name')}"
                })()
            else:
                self.user = None

    @staticmethod
    def get_by_id(photographer_id):
        """Get photographer by ID with user information."""
        photographer_data = fetch_one(
            """
            SELECT p.*,
                   u.first_name as user_first_name,
                   u.last_name as user_last_name,
                   u.email as user_email,
                   u.profile_image as user_profile_image
            FROM photographers p
            JOIN users u ON p.user_id = u.id
            WHERE p.id = %s
            """,
            (photographer_id,)
        )
        return Photographer(photographer_data) if photographer_data else None

    @staticmethod
    def get_by_user_id(user_id):
        """Get photographer by user ID with user information."""
        photographer_data = fetch_one(
            """
            SELECT p.*,
                   u.first_name as user_first_name,
                   u.last_name as user_last_name,
                   u.email as user_email,
                   u.profile_image as user_profile_image
            FROM photographers p
            JOIN users u ON p.user_id = u.id
            WHERE p.user_id = %s
            """,
            (user_id,)
        )
        return Photographer(photographer_data) if photographer_data else None

    @staticmethod
    def get_all():
        """Get all photographers with their user information."""
        photographers_data = fetch_all(
            """
            SELECT p.*,
                   u.first_name as user_first_name,
                   u.last_name as user_last_name,
                   u.email as user_email,
                   u.profile_image as user_profile_image
            FROM photographers p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC
            """
        )
        return [Photographer(p) for p in photographers_data]

    @staticmethod
    def create(user_id, bio=None, phone=None, location=None, social_link=None):
        """Create a new photographer profile."""
        photographer_id = execute_query(
            """
            INSERT INTO photographers (user_id, bio, phone, location, social_link, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, bio, phone, location, social_link, datetime.utcnow())
        )
        return Photographer.get_by_id(photographer_id)

    @staticmethod
    def update(photographer_id, **kwargs):
        """Update photographer profile."""
        allowed_fields = ['bio', 'phone', 'location', 'social_link']
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
    def delete(photographer_id):
        """Delete a photographer profile."""
        execute_query("DELETE FROM photographers WHERE id = %s", (photographer_id,))

    def __repr__(self):
        return f'<Photographer {self.id}>'


class Customer:
    """Customer profile model."""

    def __init__(self, customer_dict):
        """Initialize customer from database dictionary."""
        if customer_dict:
            self.id = customer_dict.get('id')
            self.user_id = customer_dict.get('user_id')
            self.phone = customer_dict.get('phone')
            self.address = customer_dict.get('address')
            self.created_at = customer_dict.get('created_at')

            # Create user object if user data is present
            if 'user_first_name' in customer_dict:
                self.user = type('User', (), {
                    'id': customer_dict.get('user_id'),
                    'first_name': customer_dict.get('user_first_name'),
                    'last_name': customer_dict.get('user_last_name'),
                    'email': customer_dict.get('user_email'),
                    'profile_image': customer_dict.get('user_profile_image'),
                    'full_name': f"{customer_dict.get('user_first_name')} {customer_dict.get('user_last_name')}"
                })()
            else:
                self.user = None

    @staticmethod
    def get_by_id(customer_id):
        """Get customer by ID with user information."""
        customer_data = fetch_one(
            """
            SELECT c.*,
                   u.first_name as user_first_name,
                   u.last_name as user_last_name,
                   u.email as user_email,
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
        """Get customer by user ID with user information."""
        customer_data = fetch_one(
            """
            SELECT c.*,
                   u.first_name as user_first_name,
                   u.last_name as user_last_name,
                   u.email as user_email,
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
        """Get all customers with their user information."""
        customers_data = fetch_all(
            """
            SELECT c.*,
                   u.first_name as user_first_name,
                   u.last_name as user_last_name,
                   u.email as user_email,
                   u.profile_image as user_profile_image
            FROM customers c
            JOIN users u ON c.user_id = u.id
            ORDER BY c.created_at DESC
            """
        )
        return [Customer(c) for c in customers_data]

    @staticmethod
    def create(user_id, phone=None, address=None):
        """Create a new customer profile."""
        customer_id = execute_query(
            """
            INSERT INTO customers (user_id, phone, address, created_at)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, phone, address, datetime.utcnow())
        )
        return Customer.get_by_id(customer_id)

    @staticmethod
    def update(customer_id, phone=None, address=None):
        """Update customer profile."""
        execute_query(
            "UPDATE customers SET phone = %s, address = %s WHERE id = %s",
            (phone, address, customer_id)
        )
        return Customer.get_by_id(customer_id)

    @staticmethod
    def delete(customer_id):
        """Delete a customer profile."""
        execute_query("DELETE FROM customers WHERE id = %s", (customer_id,))

    def __repr__(self):
        return f'<Customer {self.id}>'


class PortfolioItem:
    """Portfolio item model for photographer portfolios."""

    def __init__(self, portfolio_dict):
        """Initialize portfolio item from database dictionary."""
        if portfolio_dict:
            self.id = portfolio_dict.get('id')
            self.photographer_id = portfolio_dict.get('photographer_id')
            self.title = portfolio_dict.get('title')
            self.caption = portfolio_dict.get('caption')
            self.image_path = portfolio_dict.get('image_path')
            self.created_at = portfolio_dict.get('created_at')

    @staticmethod
    def get_by_id(portfolio_id):
        """Get portfolio item by ID."""
        portfolio_data = fetch_one(
            "SELECT * FROM portfolio_items WHERE id = %s",
            (portfolio_id,)
        )
        return PortfolioItem(portfolio_data) if portfolio_data else None

    @staticmethod
    def get_by_photographer(photographer_id):
        """Get all portfolio items for a photographer."""
        portfolio_data = fetch_all(
            "SELECT * FROM portfolio_items WHERE photographer_id = %s ORDER BY created_at DESC",
            (photographer_id,)
        )
        return [PortfolioItem(p) for p in portfolio_data]

    @staticmethod
    def get_all():
        """Get all portfolio items."""
        portfolio_data = fetch_all("SELECT * FROM portfolio_items ORDER BY created_at DESC")
        return [PortfolioItem(p) for p in portfolio_data]

    @staticmethod
    def create(photographer_id, title, image_path, caption=None):
        """Create a new portfolio item."""
        portfolio_id = execute_query(
            """
            INSERT INTO portfolio_items (photographer_id, title, caption, image_path, created_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (photographer_id, title, caption, image_path, datetime.utcnow())
        )
        return PortfolioItem.get_by_id(portfolio_id)

    @staticmethod
    def update(portfolio_id, title=None, caption=None, image_path=None):
        """Update portfolio item."""
        allowed_fields = {'title': title, 'caption': caption, 'image_path': image_path}
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
        """Delete a portfolio item."""
        execute_query("DELETE FROM portfolio_items WHERE id = %s", (portfolio_id,))

    def __repr__(self):
        return f'<PortfolioItem {self.title}>'