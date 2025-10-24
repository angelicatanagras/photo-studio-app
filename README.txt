Photo Studio Booking App
A Flask web application for managing photo studio bookings and appointments.

Project Structure
photo-studio-app/
├── project/          # Main application package
│   ├── __init__.py   # Flask app factory
│   ├── models.py     # Data models and database layer
│   ├── views.py      # Route handlers (controllers)
│   ├── forms.py      # Form validation
│   ├── database.sql  # Database schema with demo data
│   ├── static/       # Static assets (CSS, JS, images)
│   └── templates/    # HTML templates
├── config.py         # Configuration settings
├── database.py       # Database helper utilities
├── run.py           # Application entry point
├── requirements.txt  # Python dependencies
└── .env.example     # Environment configuration example

Setup Instructions

1. Clone the Repository
git clone <repository-url>
cd photo-studio-app

2. Create Virtual Environment
Windows (CMD)
python -m venv venv
venv\Scripts\activate.bat

Windows (PowerShell / pwsh)
python -m venv venv
.\venv\Scripts\Activate.ps1

macOS / Linux
python -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Environment Configuration
Copy the example environment file and update it with your configuration:

cp .env.example .env
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


5. Database Setup
Make sure MySQL is running and create the database:

mysql -u root -p
CREATE DATABASE photostudio_booking;
exit

6. Run Database Migrations
Apply the database schema by running the SQL migration file:

mysql -u root -p photostudio_booking < project/database.sql
Or connect to MySQL and run the migration:

mysql -u root -p
USE photostudio_booking;
SOURCE project/database.sql;
exit

This will create all tables and insert default data.

7. Run the Application
python run.py
Or using Flask CLI:

flask run
The application will be available at http://127.0.0.1:5000

Database Migrations
Applying Migrations
Run SQL migration files in order:

mysql -u root -p photostudio_booking < project/database.sql

Development
Running in Debug Mode
The application runs in debug mode by default when using python run.py with FLASK_CONFIG=development.

Project Structure Notes
models.py: Data models using raw SQL queries (User, Photographer, Booking, etc.)
views.py: Flask blueprints and route handlers
forms.py: WTForms for form validation
templates/: Jinja2 HTML templates
static/: CSS, JavaScript, and image files
database.py: Database helper utilities for executing SQL queries
Custom session-based authentication (replaces Flask-Login)

Technology Stack
Flask 3.1.0: Web framework
Flask-MySQLdb 2.0.0: MySQL database adapter
Flask-WTF 1.2.2: Form handling and validation
Werkzeug 3.1.3: Password hashing and security utilities
Bootstrap-Flask 2.4.1: Bootstrap integration for templates
Raw SQL: Direct database queries without ORM

Demo Accounts
Admin Accounts:
- admin@test.com / Admin123
- admin2@test.com / Admin567

Customer Accounts:
- customer@test.com / customer123
- customer2@test.com / Roger123

Photographer Accounts:
- photo@test.com / photo123 (Steve Philips - Wedding)
- photo2@test.com / Bryan123 (Bryan Bays - Portrait)
- events@test.com / Events123 (Emma Thompson - Events)
- pet@test.com / Pet123 (Alex Johnson - Pet)
- party@test.com / Party123 (Sarah Wilson - Party)
- maternity@test.com / Maternity123 (Lisa Anderson - Maternity)
- newborn@test.com / Newborn123 (Michael Brown - Newborn)
- branding@test.com / Branding123 (David Miller - Branding)
- sports@test.com / Sports123 (James Taylor - Sports)
- cosplay@test.com / Cosplay123 (Rachel Davis - Cosplay)
