#!/usr/bin/python3

from hbnb.app import create_app
from flask_cors import CORS

app = create_app()
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5500", "http://127.0.0.1:5500"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

if __name__ == '__main__':
    app.run(debug=True