"""Routes related to user authentication."""

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from flask.helpers import send_from_directory
from werkzeug.security import check_password_hash

auth = Blueprint("auth", __name__)


from flask import Flask, send_from_directory
app = Flask(__name__)


@auth.route("/", defaults={"path": ""})
@auth.route("/<path:path>")
def index(path):
    if session.get("authorized"):
        current_app.logger.debug("Already authorized")
        print()
        print(get_serve_dir())
        print(path)
        print()
        return send_from_directory(get_serve_dir(), path or "index.html")
    # If not logged in, redirect to login page
    return redirect(url_for("auth.login"))


@auth.route("/login")
def login():
    if session.get("authorized"):
        return redirect(url_for("auth.index"))
    return render_template(
        "index.html",
        page_title = get_translation("page_title"),
        title = get_translation("title"),
        password = get_translation("password"),
        remember_me = get_translation("remember_me"),
        login_button = get_translation("login_button"),
        )


@auth.route("/login", methods=["POST"])
def login_post():
    """Check user credentials and log in if authorized."""
    def is_authenticated(password):
        hashed_password = current_app.config.get("HASHED_PASSWORD")
        return check_password_hash(hashed_password, password)
    
    if session.get("authorized"):
        return redirect(url_for("auth.index"))
    else:
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        if is_authenticated(password):
            session["authorized"] = True
            # Make session expire when closing browser
            if not remember:
                session.permanent = False
            current_app.logger.debug("Successful login")
            return redirect(url_for("auth.index"))
        else:
            # If password is wrong, reload the page and show error message
            flash(get_translation("wrong_password"))
            return redirect(url_for("auth.login")) 


@auth.route("/logout")
def logout():
    """Remove session for current user."""
    session.clear()
    return redirect(url_for("auth.login"))


def get_translation(key):
    """Get translation string for key."""
    trans_dict = current_app.config.get("TRANSLATIONS")
    lang = current_app.config.get("LANGUAGE")
    return trans_dict.get(key, {}).get(lang, "")


def get_serve_dir():
    """Get the url to redirect to depending on the language."""
    dir_dict = current_app.config.get("SERVE_DIR")
    lang = current_app.config.get("LANGUAGE")
    return dir_dict.get(lang, "")
