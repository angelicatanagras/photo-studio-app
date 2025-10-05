# from app import create_app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)

import os
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    app.run(debug=True)
