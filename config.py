"""
Default configuration for simple-login.

Can be overridden with config.py in instance folder.
"""

import datetime

DEBUG = True
WSGI_HOST = "0.0.0.0"
WSGI_PORT = 8083

SECRET_KEY = "super secret key"
SESSION_TYPE = "filesystem"
SESSION_FILE_DIR = "instance/flask_session"
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=90)
# SESSION_COOKIE_HTTPONLY = False  # Make cookies accessible via javascript

# Create with werkzeug.security.generate_password_hash
HASHED_PASSWORD = "hashed password"

# Configurations for different hosts
HOST_CONFIG = {
    "strax.gift": {
        "lang": "sv",
        "prefix": "",
        "dir": "/some/dir",
    },
    "kalufs.lol": {
        "lang": "de",
        "prefix": "some_prefix",
        "dir": "/some/other/dir"
    }
}

FALLBACK_LANG = "sv"

# String translations
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
        "de": "Einloggen"
    },
    "wrong_password": {
        "sv": "Fel lösenord",
        "de": "Falsches Passwort"
    }
}
