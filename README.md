# 📸 Photo Studio Booking App

A comprehensive web application for booking professional photography services. Built with Flask and MySQL, featuring a complete booking system with specialized photographers across 10 different photography categories.

## 🌟 Features

- **Multi-Role System**: Customers, Photographers, and Admin dashboards
- **Specialized Photographers**: 10 professional photographers covering all major photography types
- **Service Packages**: Three-tier pricing (Basic, Standard, Premium) for each service
- **Portfolio Galleries**: Professional portfolio showcases for each photographer
- **Booking Management**: Complete cart and booking system with payment processing
- **User Authentication**: Secure login system with role-based access
- **Admin Dashboard**: Comprehensive management tools for users and bookings

## 🎯 Photography Services

| Category | Photographer | Specialization |
|----------|-------------|----------------|
| 💒 Wedding | Steve Philips | Complete wedding photography services |
| 👤 Portrait | Bryan Bays | Individual and family portrait sessions |
| 🎉 Events | Emma Thompson | Corporate events, conferences, celebrations |
| 🐕 Pet | Alex Johnson | Pet photography for dogs, cats, exotic pets |
| 🎊 Party | Sarah Wilson | Birthdays, anniversaries, special occasions |
| 🤱 Maternity | Lisa Anderson | Elegant and artistic maternity portraits |
| 👶 Newborn | Michael Brown | Safe newborn photography with specialized equipment |
| 🏢 Branding | David Miller | Corporate headshots, product photography |
| ⚽ Sports | James Taylor | Athletic events, competitions, training sessions |
| 🎭 Cosplay | Rachel Davis | Character photography, costume shoots |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd photo-studio-app
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy environment file
cp .env.example .env  # macOS/Linux
copy .env.example .env  # Windows
```

Edit `.env` file with your settings:
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
```

5. **Setup database**
```bash
# Create database
mysql -u root -p
CREATE DATABASE photostudio_booking;
exit

# Run migrations
mysql -u root -p photostudio_booking < project/database.sql
```

6. **Run the application**
```bash
python run.py
```

Visit `http://127.0.0.1:5000` to access the application.

## 🧪 Demo Accounts

The application includes pre-configured demo accounts for testing:

### 👨‍💼 Admin Accounts
| Email | Password | Role |
|-------|----------|------|
| admin@test.com | Admin123 | Admin |
| admin2@test.com | Admin567 | Admin |

### 👥 Customer Accounts
| Email | Password | Name |
|-------|----------|------|
| customer@test.com | customer123 | Katie Holmes |
| customer2@test.com | Roger123 | Roger Chavez |

### 📸 Photographer Accounts
| Email | Password | Name | Specialization |
|-------|----------|------|----------------|
| photo@test.com | photo123 | Steve Philips | Wedding |
| photo2@test.com | Bryan123 | Bryan Bays | Portrait |
| events@test.com | Events123 | Emma Thompson | Events |
| pet@test.com | Pet123 | Alex Johnson | Pet |
| party@test.com | Party123 | Sarah Wilson | Party |
| maternity@test.com | Maternity123 | Lisa Anderson | Maternity |
| newborn@test.com | Newborn123 | Michael Brown | Newborn |
| branding@test.com | Branding123 | David Miller | Branding |
| sports@test.com | Sports123 | James Taylor | Sports |
| cosplay@test.com | Cosplay123 | Rachel Davis | Cosplay |

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Authentication**: Custom session-based authentication
- **Forms**: WTForms for validation
- **Templates**: Jinja2 templating engine

## 📁 Project Structure

```
photo-studio-app/
├── project/                 # Main application package
│   ├── __init__.py         # Flask app factory
│   ├── models.py           # Data models
│   ├── views.py            # Route handlers
│   ├── forms.py            # Form validation
│   ├── database.sql        # Database schema
│   ├── static/             # Static assets
│   │   ├── css/            # Stylesheets
│   │   ├── img/            # Images
│   │   └── uploads/        # User uploads
│   └── templates/          # HTML templates
├── config.py               # Configuration
├── database.py             # Database utilities
├── run.py                  # Application entry point
└── requirements.txt        # Dependencies
```

---

DATABASE MIGRATIONS

Applying Migrations

Run SQL migration files in order:

mysql -u root -p photostudio_booking < project/database.sql

---

DEVELOPMENT
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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you have any questions or need help with the application, please open an issue or contact the development team.

---

**Built with ❤️ for photography enthusiasts**
