"""Instanciation of flask app."""

import logging
import os
import sys
import time
from pathlib import Path

from flask import Flask
from flask_cors import CORS
from flask_session import Session


def create_app():
    app = Flask(__name__)

    # Fix SCRIPT_NAME when proxied
    app.wsgi_app = ReverseProxied(app.wsgi_app)

    # Enable CORS
    CORS(app, supports_credentials=True)

    # Set default config
    app.config.from_object("config")

    # Overwrite with instance config
    instance_config = Path(app.instance_path) / "config.py"
    if instance_config.is_file():
        app.config.from_pyfile(instance_config)

    # Set root path (parent dir to simplelogin package)
    app.config["ROOT_PATH"] = Path(app.root_path).parent.absolute()

    # Configure logger
    logfmt = "%(asctime)-15s - %(levelname)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    if app.config.get("DEBUG"):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                            format=logfmt, datefmt=datefmt)
        # Stop peewee from spamming
        logging.getLogger("peewee").setLevel(logging.INFO)
    else:
        today = time.strftime("%Y-%m-%d")
        logdir = Path(app.instance_path) / "logs"
        logfile = logdir /  f"{today}.log"

        # Create log dir if it does not exist
        if not logdir.exists():
            logdir.mkdir(parents=True, exist_ok=True)

        # Create log file if it does not exist
        if not logfile.is_file():
            with open(logfile, "w") as f:
                now = time.strftime("%Y-%m-%d %H:%M:%S")
                f.write("%s CREATED DEBUG FILE\n\n" % now)

        logging.basicConfig(filename=logfile, level=logging.INFO,
                            format=logfmt, datefmt=datefmt)

    # Init session
    Session(app)

    # Register blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app



class ReverseProxied(object):
    """Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    http://flask.pocoo.org/snippets/35/

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get("HTTP_X_SCRIPT_NAME", "")
        if script_name:
            environ["SCRIPT_NAME"] = script_name
            path_info = environ["PATH_INFO"]
            if path_info.startswith(script_name):
                environ["PATH_INFO"] = path_info[len(script_name):]

        scheme = environ.get("HTTP_X_SCHEME", "")
        if scheme:
            environ["wsgi.url_scheme"] = scheme
        return self.app(environ, start_response)
