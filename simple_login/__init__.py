"""Instanciation of flask app."""

import logging
import sys
import time
from pathlib import Path

from flask import Flask
from flask_cors import CORS
from flask_session import Session

from .helpers import custom_url_for


def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app, supports_credentials=True)

    # Set default config
    app.config.from_object("config")

    # Override with instance config
    instance_config = Path(app.instance_path) / "config.py"
    if instance_config.is_file():
        app.config.from_pyfile(instance_config)

    # Set root path (parent dir to simple_login package)
    app.config["ROOT_PATH"] = Path(app.root_path).parent.absolute()

    # Configure logger
    logfmt = "%(asctime)-15s - %(levelname)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    if app.config.get("DEBUG"):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                            format=logfmt, datefmt=datefmt)
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

    # Activate helper functions for jinja
    app.jinja_env.globals.update(custom_url_for=custom_url_for)

    # Register blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
