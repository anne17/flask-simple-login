"""Routes related to user authentication."""

from flask import Blueprint, Flask, current_app, flash, redirect, render_template, request, send_from_directory, session
from flask.helpers import send_from_directory
from werkzeug.security import check_password_hash

from .helpers import custom_url_for, get_serve_dir, get_translation

auth = Blueprint("auth", __name__)
app = Flask(__name__)


@auth.route("/", defaults={"path": ""})
@auth.route("/<path:path>")
def index(path):
    if session.get("authorized"):
        current_app.logger.debug("Already authorized")
        return send_from_directory(get_serve_dir(), path or "index.html")
    # If not logged in, redirect to login page
    return redirect(custom_url_for("auth.login"))


@auth.route("/login")
def login():
    """Handle login GET request."""
    if session.get("authorized"):
        return redirect(custom_url_for("auth.index"))
    return render_template(
        "index.html",
        page_title=get_translation("page_title"),
        title=get_translation("title"),
        password=get_translation("password"),
        login_button=get_translation("login_button"),
        )


@auth.route("/login", methods=["POST"])
def login_post():
    """Check user credentials and log in if authorized."""
    def is_authenticated(password):
        hashed_password = current_app.config.get("HASHED_PASSWORD")
        return check_password_hash(hashed_password, password)
    
    if session.get("authorized"):
        return redirect(custom_url_for("auth.index"))
    else:
        password = request.form.get("password")

        if is_authenticated(password):
            session["authorized"] = True
            session.permanent = False
            current_app.logger.debug("Successful login")
            return redirect(custom_url_for("auth.index"))
        else:
            # If password is wrong, reload the page and show error message
            flash(get_translation("wrong_password"))
            return redirect(custom_url_for("auth.login")) 


@auth.route("/logout")
def logout():
    """Remove session for current user."""
    session.clear()
    return redirect(custom_url_for("auth.login"))
