# Photo Studio Booking App

A Flask web application for managing photo studio bookings and appointments.

## Project Structure

```
photostudio-booking-app/
├── models/          # Data models and database layer
├── services/        # Business logic and utilities
├── views/           # Route handlers (controllers)
├── forms/           # Form validation
├── templates/       # HTML templates
├── static/          # Static assets (CSS, JS, images)
├── migrations/      # Database migrations
├── app.py          # Application factory
├── config.py       # Configuration settings
└── run.py          # Application entry point
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd photostudio-booking-app
```

### 2. Create Virtual Environment

#### Windows (CMD)
```bash
python -m venv venv
venv\Scripts\activate.bat
```

#### Windows (PowerShell / pwsh)

```cmd
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### macOS / Linux
```powershell
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file and update it with your configuration:

```bash
cp .env.example .env
```

Edit the `.env` file with your settings:

```env
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
```

### 5. Database Setup

Make sure MySQL is running and create the database:

```bash
mysql -u root -p
CREATE DATABASE photostudio_booking;
exit
```

### 6. Run Database Migrations

Apply the database schema by running the SQL migration file:

```bash
mysql -u root -p photostudio_booking < migrations/sql/001_initial_schema.sql
```

Or connect to MySQL and run the migration:

```bash
mysql -u root -p
USE photostudio_booking;
SOURCE migrations/sql/001_initial_schema.sql;
exit
```

This will create all tables and insert default roles (customer, photographer, admin).

### 7. Run the Application

```bash
python run.py
```

Or using Flask CLI:

```bash
flask run
```

The application will be available at `http://127.0.0.1:5000`

## Database Migrations

### Applying Migrations

Run SQL migration files in order:

```bash
mysql -u root -p photostudio_booking < migrations/sql/001_initial_schema.sql
```

## Development

### Running in Debug Mode

The application runs in debug mode by default when using `python run.py` with `FLASK_CONFIG=development`.

### Project Structure Notes

- **models/**: Data models using raw SQL queries (User, Photographer, Booking, etc.)
- **services/**: Business logic, helpers, and email utilities
- **views/**: Flask blueprints and route handlers
- **forms/**: WTForms for form validation
- **templates/**: Jinja2 HTML templates
- **static/**: CSS, JavaScript, and image files
- **database.py**: Database helper utilities for executing SQL queries
- **auth_utils.py**: Custom session-based authentication (replaces Flask-Login)

## Technology Stack

- **Flask 3.1.0**: Web framework
- **Flask-MySQLdb 2.0.0**: MySQL database adapter
- **Flask-WTF 1.2.2**: Form handling and validation
- **Werkzeug 3.1.3**: Password hashing and security utilities
- **Bootstrap-Flask 2.4.1**: Bootstrap integration for templates
- **Raw SQL**: Direct database queries without ORM