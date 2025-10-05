from flask import g
from contextlib import contextmanager


def get_db():
    """Get database connection from Flask-MySQLdb."""
    from .app import mysql
    return mysql


@contextmanager
def get_cursor(commit=False):
    """
    Context manager for database cursor.

    Args:
        commit (bool): Whether to commit the transaction after executing.

    Usage:
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
    """
    from MySQLdb.cursors import DictCursor
    mysql = get_db()
    cursor = mysql.connection.cursor(DictCursor)
    try:
        yield cursor
        if commit:
            mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        raise e
    finally:
        cursor.close()


def execute_query(query, params=None, commit=True):
    """
    Execute a query that modifies data (INSERT, UPDATE, DELETE).

    Args:
        query (str): SQL query with %s placeholders
        params (tuple): Parameters for the query
        commit (bool): Whether to commit the transaction

    Returns:
        int: Last inserted row ID for INSERT queries, or affected row count

    Example:
        execute_query("INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                     ("user@example.com", "hashed_password"))
    """
    with get_cursor(commit=commit) as cursor:
        cursor.execute(query, params or ())
        if query.strip().upper().startswith('INSERT'):
            return cursor.lastrowid
        return cursor.rowcount


def fetch_one(query, params=None):
    """
    Fetch a single row from the database.

    Args:
        query (str): SQL query with %s placeholders
        params (tuple): Parameters for the query

    Returns:
        dict or None: Single row as dictionary, or None if not found

    Example:
        user = fetch_one("SELECT * FROM users WHERE email = %s", ("user@example.com",))
    """
    with get_cursor() as cursor:
        cursor.execute(query, params or ())
        row = cursor.fetchone()
        return row if row else None


def fetch_all(query, params=None):
    """
    Fetch all rows from the database.

    Args:
        query (str): SQL query with %s placeholders
        params (tuple): Parameters for the query

    Returns:
        list: List of dictionaries, one per row

    Example:
        users = fetch_all("SELECT * FROM users WHERE role_id = %s", (1,))
    """
    with get_cursor() as cursor:
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        return rows if rows else []


def fetch_value(query, params=None):
    """
    Fetch a single value from the database.

    Args:
        query (str): SQL query that returns a single value
        params (tuple): Parameters for the query

    Returns:
        Any: The single value, or None if not found

    Example:
        count = fetch_value("SELECT COUNT(*) FROM users")
    """
    with get_cursor() as cursor:
        cursor.execute(query, params or ())
        row = cursor.fetchone()
        if row:
            return row[0]
        return None


def execute_many(query, params_list):
    """
    Execute the same query multiple times with different parameters.

    Args:
        query (str): SQL query with %s placeholders
        params_list (list): List of parameter tuples

    Returns:
        int: Number of affected rows

    Example:
        execute_many("INSERT INTO roles (name) VALUES (%s)",
                    [("admin",), ("photographer",), ("customer",)])
    """
    with get_cursor(commit=True) as cursor:
        cursor.executemany(query, params_list)
        return cursor.rowcount
