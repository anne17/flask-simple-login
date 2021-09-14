"""Some helper functions."""

from flask import current_app, request, url_for


def get_host_config():
    """Get correct config depending on host url."""
    host = request.host_url.split("/")[2]
    return current_app.config.get("HOST_CONFIG").get(host, {})


def get_translation(key):
    """Get translation string for key."""
    lang = get_host_config().get("lang", "")
    if not lang:
        lang = current_app.config.get("FALLBACK_LANG")
    trans_dict = current_app.config.get("TRANSLATIONS")
    return trans_dict.get(key, {}).get(lang, "")


def get_serve_dir():
    """Get the url to redirect to depending on the language."""
    return get_host_config().get("dir", "")


def custom_url_for(url, filename=None):
    """Get URL including the host prefix."""
    config = get_host_config()
    host_url = request.host_url.rstrip("/")
    return host_url + config.get("prefix", "") + url_for(url, filename=filename)
