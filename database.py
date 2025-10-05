from flask import g
from contextlib import contextmanager


def get_db():
    from .app import mysql
    return mysql


@contextmanager
def get_cursor(commit=False):
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
    """Returns last inserted ID for INSERT, row count for others."""
    with get_cursor(commit=commit) as cursor:
        cursor.execute(query, params or ())
        if query.strip().upper().startswith('INSERT'):
            return cursor.lastrowid
        return cursor.rowcount


def fetch_one(query, params=None):
    with get_cursor() as cursor:
        cursor.execute(query, params or ())
        row = cursor.fetchone()
        return row if row else None


def fetch_all(query, params=None):
    with get_cursor() as cursor:
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        return rows if rows else []


def fetch_value(query, params=None):
    with get_cursor() as cursor:
        cursor.execute(query, params or ())
        row = cursor.fetchone()
        if row:
            return row[0]
        return None


def execute_many(query, params_list):
    with get_cursor(commit=True) as cursor:
        cursor.executemany(query, params_list)
        return cursor.rowcount
