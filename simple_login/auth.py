"""Routes related to user authentication."""

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/")
def index():
    return redirect(url_for("auth.check_login"))


@auth.route("/login")
def login():
    if session.get("authorized"):
        return redirect(get_main_url())
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
        return redirect(get_main_url())
    else:
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        if is_authenticated(password):
            session["authorized"] = True
            # Make session expire when closing browser
            if not remember:
                session.permanent = False
            current_app.logger.debug("Successful login")
            return redirect(get_main_url())
        else:
            # If password is wrong, reload the page and show error message
            flash(get_translation("wrong_password"))
            return redirect(url_for("auth.login")) 


@auth.route("/check-login")
def check_login():
    """Check if current user is authorized in the active session."""
    if session.get("authorized"):
        current_app.logger.debug("Successful login")
        return redirect(get_main_url())
    else:
        # If not logged in, redirect to login page
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


def get_main_url():
    """Get the url to redirect to depending on the language."""
    url_dict = current_app.config.get("MAIN_PAGES")
    lang = current_app.config.get("LANGUAGE")
    return url_dict.get(lang, "")
