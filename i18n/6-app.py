#!/usr/bin/env python3
"""
Use user locale preference with priority order
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel


app = Flask(__name__)


class Config(object):
    """
    Config class for Babel
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """
    Return a user dict from login_as query param, or None
    """
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """
    Set the logged-in user on flask.g before each request
    """
    g.user = get_user()


def get_locale():
    """
    Determine locale with priority:
    1. URL parameter
    2. User settings
    3. Request Accept-Language header
    4. Default locale
    """
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale

    if g.user and g.user.get("locale") in app.config["LANGUAGES"]:
        return g.user["locale"]

    return request.accept_languages.best_match(app.config["LANGUAGES"])


babel = Babel()
babel.init_app(app, locale_selector=get_locale)


@app.route("/")
def index():
    """
    Render the index template
    """
    return render_template("6-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
