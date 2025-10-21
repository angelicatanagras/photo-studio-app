import os

basedir = os.path.abspath(os.path.dirname(__file__))

env_file = os.path.join(basedir, '.env')
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Flask-MySQLdb Configuration
    MYSQL_HOST = os.environ.get('DB_HOST') or 'localhost'
    MYSQL_PORT = int(os.environ.get('DB_PORT') or 3306)
    MYSQL_DB = os.environ.get('DB_NAME') or 'photostudio_booking'
    MYSQL_USER = os.environ.get('DB_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('DB_PASSWORD') or ''
    MYSQL_CURSORCLASS = 'DictCursor'

    # Upload Configuration
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads', 'portfolio')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 5MB max file size

    PROFILE_IMAGE_FOLDER = os.path.join(basedir, 'static', 'uploads', 'profiles')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(basedir, 'static', 'uploads', 'portfolio')
    PROFILE_IMAGE_FOLDER = os.environ.get('PROFILE_IMAGE_FOLDER') or os.path.join(basedir, 'static', 'uploads', 'profiles')


class TestingConfig(Config):
    TESTING = True
    MYSQL_DB = 'photostudio_booking_test'

    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(basedir, 'static', 'uploads', 'portfolio')
    PROFILE_IMAGE_FOLDER = os.environ.get('PROFILE_IMAGE_FOLDER') or os.path.join(basedir, 'static', 'uploads', 'profiles')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
