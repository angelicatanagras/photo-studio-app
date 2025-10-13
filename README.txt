Photo Studio Booking App - Setup Instructions
==============================================

1. Create Virtual Environment:
   - Windows: python -m venv venv && venv\Scripts\activate
   - macOS/Linux: python -m venv venv && source venv/bin/activate

2. Install Dependencies:
   pip install -r requirements.txt

3. Configure Environment:
   - Copy .env.example to .env
   - Update database credentials in .env file

4. Setup Database:
   - Create MySQL database: CREATE DATABASE photostudio_booking;
   - Import schema: mysql -u root -p photostudio_booking < project/database.sql

5. Run Application:
   python run.py

6. Access Application:
   Open browser to http://127.0.0.1:5000

Default Credentials:
- Admin: admin@test.com / Admin123
- Customer: customer@test.com / customer123
- Photographer: photo@test.com / photo123

Technology Stack:
- Flask 3.1.0
- Flask-MySQLdb 2.0.0
- Flask-WTF 1.2.2
- Bootstrap-Flask 2.4.1
