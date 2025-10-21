================================================================================
PHOTO STUDIO BOOKING APP
================================================================================
PROJECT STRUCTURE
================================================================================

photo_studio_app/
├── project/              # Main application package
│   ├── __init__.py      # Flask app factory
│   ├── models.py        # Data models (User, Photographer, Booking, etc.)
│   ├── views.py         # Route handlers with blueprints
│   ├── forms.py         # WTForms validation
│   ├── database.sql     # Database schema with demo data
│   ├── static/          # Static assets (CSS, images, uploads)
│   └── templates/       # Jinja2 HTML templates
├── config.py            # Flask configuration
├── database.py          # Database helper utilities
├── run.py              # Application entry point
├── requirements.txt     # Python dependencies
└── .env.example        # Environment configuration example

================================================================================
SETUP INSTRUCTIONS
================================================================================

1. Clone the Repository
--------------------------------------------------------------------------------

git clone <repository-url>
cd photo_studio_app


2. Create Virtual Environment
--------------------------------------------------------------------------------

Windows (CMD):
    python -m venv venv
    venv\Scripts\activate.bat

Windows (PowerShell):
    python -m venv venv
    .\venv\Scripts\Activate.ps1

macOS / Linux:
    python -m venv venv
    source venv/bin/activate


3. Install Dependencies
--------------------------------------------------------------------------------

pip install -r requirements.txt


4. Environment Configuration
--------------------------------------------------------------------------------

Copy the example environment file and update it with your configuration:

    cp .env.example .env          (macOS/Linux)
    copy .env.example .env        (Windows)

Edit the .env file with your settings:

# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_CONFIG=development

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=photostudio_booking
DB_USER=root
DB_PASSWORD=your-mysql-password

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password


5. Database Setup
--------------------------------------------------------------------------------

Make sure MySQL is running and create the database:

mysql -u root -p
CREATE DATABASE photostudio_booking;
exit


6. Run Database Migrations
--------------------------------------------------------------------------------

Apply the database schema by running the SQL migration file:

    mysql -u root -p photostudio_booking < project/database.sql

Or connect to MySQL and run the migration:

    mysql -u root -p
    USE photostudio_booking;
    SOURCE project/database.sql;
    exit

This will create all tables and insert default data.


7. Run the Application
--------------------------------------------------------------------------------

python run.py

Or using Flask CLI:

    flask run

The application will be available at http://127.0.0.1:5000

================================================================================
DATABASE MIGRATIONS
================================================================================

Applying Migrations

Run SQL migration files in order:

mysql -u root -p photostudio_booking < project/database.sql

================================================================================
DEVELOPMENT
================================================================================

Running in Debug Mode

The application runs in debug mode by default when using `python run.py`
with FLASK_CONFIG=development.

Project Structure Notes

- models/: Data models using raw SQL queries (User, Photographer, Booking, etc.)
- views/: Flask blueprints and route handlers
- forms/: WTForms for form validation
- templates/: Jinja2 HTML templates
- static/: CSS, JavaScript, and image files
- database.py: Database helper utilities for executing SQL queries
- Custom session-based authentication (replaces Flask-Login)

================================================================================
