import os
from project import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'production')

if __name__ == '__main__':
    app.run(debug=False)
