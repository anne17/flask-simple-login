"""
Default configuration for simple-login backend.

Can be overwritten with config.py in instance folder.
"""

import datetime

DEBUG = True
WSGI_HOST = "0.0.0.0"
WSGI_PORT = 9005

SECRET_KEY = "super secret key"
SESSION_TYPE = "filesystem"
SESSION_FILE_DIR = "instance/flask_session"
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=90)

# Create with werkzeug.security.generate_password_hash
HASHED_PASSWORD = "hashed password"

LANGUAGE = "sv"

MAIN_PAGES = {
    "sv": "https://google.com",
    "de": "https://google.com"
    }


TRANSLATIONS = {
    "page_title": {
        "sv": "Login",
        "de": "Login"
    },
    "title": {
        "sv": "Inloggning",
        "de": "Login"
    },
    "password": {
        "sv": "Lösenord",
        "de": "Passwort"
    },
    "remember_me": {
        "sv": "Kom ihåg mig",
        "de": "Eingeloggt bleiben"
    },
    "login_button": {
        "sv": "Logga in",
        "de": "Login"
    },
    "wrong_password": {
        "sv": "Fel lösenord",
        "de": "Falsches Passwort"
    }
}
