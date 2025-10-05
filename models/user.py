from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ..database import fetch_one, fetch_all, execute_query


class Role:
    """Role model for user roles (admin, photographer, customer)."""

    @staticmethod
    def get_by_id(role_id):
        """Get a role by ID."""
        return fetch_one("SELECT * FROM roles WHERE id = %s", (role_id,))

    @staticmethod
    def get_by_name(name):
        """Get a role by name."""
        return fetch_one("SELECT * FROM roles WHERE name = %s", (name,))

    @staticmethod
    def get_all():
        """Get all roles."""
        return fetch_all("SELECT * FROM roles")

    @staticmethod
    def create(name):
        """Create a new role."""
        role_id = execute_query(
            "INSERT INTO roles (name) VALUES (%s)",
            (name,)
        )
        return Role.get_by_id(role_id)


class User:
    """User model for authentication and user management."""

    def __init__(self, user_dict):
        """Initialize user from database dictionary."""
        if user_dict:
            self.id = user_dict.get('id')
            self.email = user_dict.get('email')
            self.password_hash = user_dict.get('password_hash')
            self.first_name = user_dict.get('first_name')
            self.last_name = user_dict.get('last_name')
            self.profile_image = user_dict.get('profile_image')
            self.role_id = user_dict.get('role_id')
            self.created_at = user_dict.get('created_at')

    @property
    def full_name(self):
        """Get user's full name."""
        return f'{self.first_name} {self.last_name}'

    def set_password(self, password):
        """Hash and set password."""
        return generate_password_hash(password, method='pbkdf2:sha256')

    @staticmethod
    def check_password(password_hash, password):
        """Check if password matches hash."""
        return check_password_hash(password_hash, password)

    @staticmethod
    def get_by_id(user_id):
        """Get a user by ID."""
        user_data = fetch_one("SELECT * FROM users WHERE id = %s", (user_id,))
        return User(user_data) if user_data else None

    @staticmethod
    def get_by_email(email):
        """Get a user by email."""
        user_data = fetch_one("SELECT * FROM users WHERE email = %s", (email,))
        return User(user_data) if user_data else None

    @staticmethod
    def get_all():
        """Get all users."""
        users_data = fetch_all("SELECT * FROM users")
        return [User(user) for user in users_data]

    @staticmethod
    def create(email, password, first_name, last_name, role_id, profile_image=None):
        """Create a new user."""
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        user_id = execute_query(
            """
            INSERT INTO users (email, password_hash, first_name, last_name,
                              profile_image, role_id, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (email, password_hash, first_name, last_name, profile_image,
             role_id, datetime.utcnow())
        )
        return User.get_by_id(user_id)

    @staticmethod
    def update(user_id, **kwargs):
        """Update user fields."""
        allowed_fields = ['email', 'first_name', 'last_name', 'profile_image', 'role_id']
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
        """Update user's password."""
        password_hash = generate_password_hash(new_password, method='pbkdf2:sha256')
        execute_query(
            "UPDATE users SET password_hash = %s WHERE id = %s",
            (password_hash, user_id)
        )

    @staticmethod
    def delete(user_id):
        """Delete a user."""
        execute_query("DELETE FROM users WHERE id = %s", (user_id,))

    def __repr__(self):
        return f'<User {self.email}>'